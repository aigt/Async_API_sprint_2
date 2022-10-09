import functools
import logging
import uuid as uuid_m
from typing import Any

from fastapi import Depends, Path

from api.v1.schemas import Person
from cache import cached
from models.elastic.person import Person as ElasticPerson
from models.elastic.person import Role as ElasticRole
from repositories.elastic import ElastisearchRepository, get_person_repository
from services.person.person_list_query_body import (person_list_query_body,
                                                    person_search_query_body)


def _reduce_person_role(roles_acc: dict[str, set[Any]], role: ElasticRole) -> dict:
    roles_acc['film_ids'].add(role.film_id)
    roles_acc['role'].add(role.role)
    return roles_acc


def _map_person(person: ElasticPerson) -> Person:
    roles = functools.reduce(
        _reduce_person_role,
        person.roles,
        {'film_ids': set(), 'role': set()},
    )
    return Person(
        uuid=person.id,
        full_name=person.full_name,
        film_ids=list(roles['film_ids']),
        role=list(roles['role']),
    )


async def _person_list_by_query(
    query_body: dict,
    person_repo: ElastisearchRepository[ElasticPerson],
) -> list[Person]:
    persons = await person_repo.list(query_body=query_body)
    return [_map_person(person) for person in persons]


async def get_person_list(
    query_body: dict = Depends(person_list_query_body),
    person_repo: ElastisearchRepository[ElasticPerson] = Depends(get_person_repository),
) -> list[Person]:
    return await _person_list_by_query(
        query_body=query_body,
        person_repo=person_repo,
    )


async def search_person(
    query_body: dict = Depends(person_search_query_body),
    person_repo: ElastisearchRepository[ElasticPerson] = Depends(get_person_repository),
) -> list[Person]:
    return await _person_list_by_query(
        query_body=query_body,
        person_repo=person_repo,
    )


@cached.cached_id_item(id_name='person_id')
async def get_person_by_id(
    person_id: uuid_m.UUID = Path(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым фильм хранится в БД",
    ),
    person_repo: ElastisearchRepository[ElasticPerson] = Depends(get_person_repository),
) -> Person | None:
    person = await person_repo.get_by_id(person_id)
    if not person:
        return None
    return _map_person(person)
