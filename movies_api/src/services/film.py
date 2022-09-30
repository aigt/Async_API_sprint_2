import logging
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.elastic.film import Film
from services.film_list_query_config import FilmListQueryConfig


async def film_list_es_query(query_config: FilmListQueryConfig):
    # Пагинация
    body = {
        'size': query_config.page.size,
        'from': (query_config.page.number - 1) * query_config.page.size,
    }

    # Добавь сортировку, если требуется
    if query_config.sort is not None:
        body['sort'] = {
            query_config.sort.field: {
                'order': query_config.sort.order,
            },
        }

    # Добавь запрос и/или фильтрацию
    if query_config.bool_q is not None:
        boolean_query = {}
        body['query'] = {'bool': boolean_query}
        # Фильтрация
        if query_config.bool_q.filter is not None:
            # Выбор по какому полю фильтровать
            match query_config.bool_q.filter.field:
                case 'genre':
                    boolean_query['filter'] = {
                        'match': {'genre': query_config.bool_q.filter.value},
                    }
        # Запрос
        if query_config.bool_q.query is not None:
            boolean_query['must'] = {
                'query_string': {
                    'query': query_config.bool_q.query,
                    'fields': ['title', 'description'],
                },
            }

    # Выборка всех, если нет запроса или фильтрации
    body.setdefault('query', {'match_all': {}})

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
        return films

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        return await self._get_film_from_elastic(film_id)

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
