from http import HTTPStatus
import uuid as uuid_m

from fastapi import APIRouter, Depends, HTTPException, Query, Path

from api.v1.schemas import Person
from cache import cached
from core import text_messages
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/search",
    response_model=list[Person],
    summary="Найти персоны по запросу",
)
async def persons_search(
    query: str,
    page_size: int = Query(
        default=20,
        alias="page[size]",
    ),
    page_number: int
    | None = Query(
        default=1,
        alias="page[number]",
    ),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    """
    Найти персону по запросу с полной информацией:

    - **uuid**: идентификатор
    - **full_name**: название фильма
    - **film_ids**: imdb рейтинг фильма
    - **role**: жанры фильма
    """

    persons = await person_service.search_person(query, page_number, page_size)

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.PERSONS_NOT_FOUND,
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


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Получить персону",
)
@cached.cached_id_item(id_name='person_id')
async def person_details(
    person_id: uuid_m.UUID = Path(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым персона хранится в БД",
    ),
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    """
    Получить персону с полной информацией:

    - **uuid**: идентификатор
    - **full_name**: название фильма
    - **film_ids**: imdb рейтинг фильма
    - **role**: жанры фильма
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=text_messages.PERSON_NOT_FOUND
        )
    return Person(
        uuid=person.id,
        full_name=person.full_name,
        film_ids=person.film_ids,
        role=person.role,
    )


@router.get(
    "/",
    response_model=list[Person],
    summary="Получить список персон",
)
async def persons_list(
    page_size: int = Query(
        default=20,
        alias="page[size]",
    ),
    page_number: int = Query(
        default=1,
        alias="page[number]",
    ),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    """
    Получить список персон с полной информацией:

    - **uuid**: идентификатор
    - **full_name**: название фильма
    - **film_ids**: imdb рейтинг фильма
    - **role**: жанры фильма
    """

    persons = await person_service.list(page_size, page_number)

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.PERSONS_NOT_FOUND,
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
