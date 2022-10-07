from functools import lru_cache
from typing import Generic, TypeVar

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.elastic.film import Film
from models.elastic.genre import Genre
from models.elastic.person import Person

TItem = TypeVar('TItem')

class ElastisearchRepository(Generic[TItem]):
    def __init__(self, elastic: AsyncElasticsearch, index: str) -> None:
        self._elastic = elastic
        self._index = index
        
    async def get_by_id(self, id: str) -> TItem:
        try:
            doc = await self._elastic.get(index=self._index, id=id)
        except NotFoundError:
            return None
        TItem_type = self.__orig_class__.__args__[0]
        return TItem_type(**doc['_source'])
    
    async def list(self, query_body: dict) -> list[TItem]:
        resp = await self._elastic.search(index=self._index, body=query_body)
        TItem_type = self.__orig_class__.__args__[0]
        items = [TItem_type(**film_doc['_source']) for film_doc in resp['hits']['hits']]
        return items


@lru_cache()
def get_film_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElastisearchRepository:
    return ElastisearchRepository[Film](elastic=elastic, index='movies')

@lru_cache()
def get_genre_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElastisearchRepository:
    return ElastisearchRepository[Genre](elastic=elastic, index='genres')

@lru_cache()
def get_person_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElastisearchRepository:
    return ElastisearchRepository[Person](elastic=elastic, index='persons')
