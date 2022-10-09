from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas import Person
from core import text_messages
from services import person as service

router = APIRouter()


@router.get(
    "/search",
    response_model=list[Person],
    summary="Найти персоны по запросу",
)
async def persons_search(
    person_list: list[Person] = Depends(service.search_person),
) -> list[Person]:
    """
    Найти персону по запросу с полной информацией:

    - **uuid**: идентификатор
    - **full_name**: название фильма
    - **film_ids**: imdb рейтинг фильма
    - **role**: жанры фильма
    """
    if not person_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.PERSONS_NOT_FOUND,
        )
    return person_list


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Получить персону",
)
async def person_details(
    person: Person | None = Depends(service.get_person_by_id),
) -> Person:
    """
    Получить персону с полной информацией:

    - **uuid**: идентификатор
    - **full_name**: название фильма
    - **film_ids**: imdb рейтинг фильма
    - **role**: жанры фильма
    """
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.PERSON_NOT_FOUND,
        )
    return person


@router.get(
    "/",
    response_model=list[Person],
    summary="Получить список персон",
)
async def persons_list(
    person_list: list[Person] = Depends(service.get_person_list),
) -> list[Person]:
    """
    Получить список персон с полной информацией:

    - **uuid**: идентификатор
    - **full_name**: название фильма
    - **film_ids**: imdb рейтинг фильма
    - **role**: жанры фильма
    """
    if not person_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.PERSONS_NOT_FOUND,
        )
    return person_list
