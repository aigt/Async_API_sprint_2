from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis


GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5

#подключаем выдачу жанров списком
from services.genre_list_query_config import GenreListQueryConfig
from models.genre import Genre


async def genre_list_es_query(query_config: GenreListQueryConfig):
    body = {
        'size': query_config.page.size,
        'from': (query_config.page.number - 1) * query_config.page.size,
        'query': {
            'match_all': {},
        },
    }
    return body




class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def list(self, query_config: GenreListQueryConfig) -> list[Genre]:
        body = await genre_list_es_query(query_config)
        resp = await self.elastic.search(index="genres", body=body)
        genres = [Genre(**genre_doc['_source']) for genre_doc in resp['hits']['hits']]
        return genres

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(str(genre.id), genre.json(), ex=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
