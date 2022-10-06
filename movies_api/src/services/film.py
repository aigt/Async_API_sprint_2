from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.elastic.film import Film


class FilmService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic
        self.index='movies'

    async def list(
        self,
        query_body: dict,
    ) -> list[Film]:
        resp = await self.elastic.search(index=self.index, body=query_body)
        films = [Film(**film_doc['_source']) for film_doc in resp['hits']['hits']]
        return films

    async def get_by_id(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index=self.index, id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
