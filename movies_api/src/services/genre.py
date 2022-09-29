from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis

from models.genre import Genre


GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def list(self, page_number, page_size) -> list[Genre]:
        from_value = None
        if page_size and page_size:
            from_value = int(page_number) * int(page_size) - 3
        query_body = {
            "query": {"match_all": {}},
            "size": page_size,
            "from": from_value
        }
        resp = await self.elastic.search(index="genres", body=query_body)
        genres = [Genre(**genre_doc["_source"]) for genre_doc in resp["hits"]["hits"]]
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
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(
            str(genre.id), genre.json(), ex=GENRE_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
