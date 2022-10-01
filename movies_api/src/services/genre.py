from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.elastic.genre import Genre


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def list(self, page_number, page_size) -> list[Genre]:
        from_value = None
        if page_size and page_size:
            from_value = int(page_number) * int(page_size) - 3
        query_body = {"query": {"match_all": {}}, "size": page_size, "from": from_value}
        resp = await self.elastic.search(index="genres", body=query_body)
        genres = [Genre(**genre_doc["_source"]) for genre_doc in resp["hits"]["hits"]]
        return genres

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        return await self._get_genre_from_elastic(genre_id)

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
