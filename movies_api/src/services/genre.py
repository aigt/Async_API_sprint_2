from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.elastic.genre import Genre


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def list(self, page_number: int, page_size: int) -> list[Genre]:
        from_value = None
        if page_size and page_size:
            from_value = (page_number - 1) * page_size
        query_body = {"query": {"match_all": {}}, "size": page_size, "from": from_value}
        resp = await self.elastic.search(index="genres", body=query_body)
        genres = [Genre(**genre_doc["_source"]) for genre_doc in resp["hits"]["hits"]]
        return genres

    async def get_by_id(self, genre_id: str) -> Genre | None:
        return await self._get_genre_from_elastic(genre_id)

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
