import uuid

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List

from services.person import PersonService, get_person_service
from services.film_list_query_config import FilmListQueryConfig, film_list_query_config


router = APIRouter()


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    film_ids: List | None
    role: List | None | str


@router.get("/")
async def persons_list(
    query_config: FilmListQueryConfig = Depends(film_list_query_config),
    person_service: PersonService = Depends(get_person_service),
    q: str | None = Query(default=None, alias="query"),
    page_size: str | None = Query(default=None, alias="page[number]"),
    page_number: str | None = Query(default=None, alias="page[size]"),
) -> List[Person]:

    persons = await person_service.search_person(q, page_number, page_size)

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="persons not found",
        )
    return [
        Person(
            uuid=person.id, full_name=person.full_name, film_ids=person.film_ids, role=person.role
        )
        for person in persons
    ]
