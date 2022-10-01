import uuid
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import BaseModel

from db.elastic import get_elastic
from db.redis import get_redis
from models.elastic.person import Person
from models.es_query_configs.film_list_query_config import FilmListQueryConfig
from services.film import film_list_es_query


class Movie(BaseModel):
    id: uuid.UUID


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_persons_films(self, name: str):
        query_body = {
            "query": {
                "multi_match": {
                    "query": name,
                    "fields": ["actors_names", "writers_names", "director"],
                }
            }
        }
        resp = await self.elastic.search(index="movies", body=query_body)
        persons_films = [
            Movie(**film_doc["_source"]).id for film_doc in resp["hits"]["hits"]
        ]
        return persons_films

    async def get_persons_roles(self, name: str, role_to_check: str):
        check_role_query = {
            "query": {"bool": {"must": {"match": {role_to_check: name}}}}
        }

        resp = await self.elastic.search(index="movies", body=check_role_query)
        roles_list = [
            Movie(**film_doc["_source"]).id for film_doc in resp["hits"]["hits"]
        ]
        return roles_list

    async def list(self, query_config: FilmListQueryConfig):
        body = await film_list_es_query(query_config)
        resp = await self.elastic.search(index="persons", body=body)
        persons = [
            Person(**person_doc["_source"]) for person_doc in resp["hits"]["hits"]
        ]

        for person in persons:
            person_films = await self.get_persons_films(person.full_name)
            person.film_ids = person_films

            is_director = await self.get_persons_roles(person.full_name, "director")
            is_actor = await self.get_persons_roles(person.full_name, "actors_names")
            is_writer = await self.get_persons_roles(person.full_name, "writers_names")

            roles = []
            if is_director:
                roles.append("Director")
            if is_actor:
                roles.append("Actor")
            if is_writer:
                roles.append("Writer")
            person.role = roles

        return persons

    async def search_person(self, query, page_number, page_size):
        from_value = None
        if page_size and page_size:
            from_value = int(page_number) * int(page_size) - 3
        query_body = {
            "query": {"multi_match": {"query": query, "fields": ["full_name"]}},
            "size": page_size,
            "from": from_value,
        }
        resp = await self.elastic.search(index="persons", body=query_body)
        persons = [
            Person(**person_doc["_source"]) for person_doc in resp["hits"]["hits"]
        ]

        for person in persons:
            person_films = await self.get_persons_films(person.full_name)
            person.film_ids = person_films

            is_director = await self.get_persons_roles(person.full_name, "director")
            is_actor = await self.get_persons_roles(person.full_name, "actors_names")
            is_writer = await self.get_persons_roles(person.full_name, "writers_names")

            roles = []
            if is_director:
                roles.append("Director")
            if is_actor:
                roles.append("Actor")
            if is_writer:
                roles.append("Writer")
            person.role = roles

        return persons

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._get_person_from_elastic(person_id)

        person.film_ids = await self.get_persons_films(person.full_name)

        is_director = await self.get_persons_roles(person.full_name, "director")
        is_actor = await self.get_persons_roles(person.full_name, "actors_names")
        is_writer = await self.get_persons_roles(person.full_name, "writers_names")

        roles = []
        if is_director:
            roles.append("Director")
        if is_actor:
            roles.append("Actor")
        if is_writer:
            roles.append("Writer")
        person.role = roles

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
