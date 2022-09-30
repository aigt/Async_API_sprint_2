import uuid
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from cache import cached
from services.film_list_query_config import FilmListQueryConfig, film_list_query_config
from services.person import PersonService, get_person_service

router = APIRouter()


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    film_ids: List | None
    role: List | None


@router.get("/search", response_model=List[Person])
async def persons_search(
    query: str,
    page_size: str | None = Query(default=None, alias="page[size]"),
    page_number: str | None = Query(default=None, alias="page[number]"),
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:

    persons = await person_service.search_person(query, page_number, page_size)

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="persons not found",
        )
    return [
        Person(
            uuid=person.id,
            full_name=person.full_name,
            film_ids=person.film_ids,
            role=person.role,
        )
        for person in persons
    ]


@router.get("/{person_id}", response_model=Person)
@cached.cached_id_item(id_name='person_id')
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return Person(
        uuid=person.id,
        full_name=person.full_name,
        film_ids=person.film_ids,
        role=person.role,
    )


@router.get("/")
async def persons_list(
    query_config: FilmListQueryConfig = Depends(film_list_query_config),
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:

    persons = await person_service.list(query_config)

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="persons not found",
        )
    return [
        Person(
            uuid=person.id,
            full_name=person.full_name,
            film_ids=person.film_ids,
            role=person.role,
        )
        for person in persons
    ]
