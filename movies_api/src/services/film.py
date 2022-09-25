import logging
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.elastic.film import Film
from services.film_list_query_config import FilmListQueryConfig

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


async def film_list_es_query(query_config: FilmListQueryConfig):
    body = {
        'size': query_config.page.size,
        'from': (query_config.page.number - 1) * query_config.page.size,
        'query': {
            'match_all': {},
        },
    }
    logging.info(body)

    if query_config.sort is not None:
        body['sort'] = {
            query_config.sort.field: {
                'order': query_config.sort.order,
            },
        }

    if query_config.filter is not None:
        match query_config.filter.field:
            case 'genre':
                body['query'] = {
                    'bool': {
                        'filter': {
                            'term': {
                                'genre': query_config.filter.value,
                            }
                        },
                    }
                }

    return body


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def list(
        self,
        query_config: FilmListQueryConfig,
    ) -> list[Film]:

        logging.info(query_config)

        body = await film_list_es_query(query_config)

        resp = await self.elastic.search(index="movies", body=body)
        logging.info(resp)

        films = [Film(**film_doc['_source']) for film_doc in resp['hits']['hits']]
        # logging.info(films)
        return films

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может
    # отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще
                # нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(film_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из
        # json
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(
            str(film.id),
            film.json(),
            ex=FILM_CACHE_EXPIRE_IN_SECONDS,
        )


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
