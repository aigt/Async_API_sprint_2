from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas import Film
from core import text_messages
from services import film as service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[Film],
    summary="Найти фильмы по запросу",
)
async def search_films(
    film_list: list[Film] = Depends(service.search_films),
) -> list[Film]:
    """
    Найти фильмы по запросу с полной информацией:

    - **id**: идентификатор
    - **title**: название фильма
    - **imdb_rating**: imdb рейтинг фильма
    - **genre**: жанры фильма
    - **description**: описание фильма
    - **actors**: актёры
    - **writers**: сценаристы
    - **director**: режиссёры
    """
    if not film_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.FILMS_NOT_FOUND,
        )
    return film_list


@router.get(
    '/{film_id}',
    response_model=Film,
    summary="Получить фильм",
)
async def get_film_by_id(
    film: Film = Depends(service.get_film_by_id),
) -> Film:
    """
    Получить фильм с полной информацией:

    - **id**: идентификатор
    - **title**: название фильма
    - **imdb_rating**: imdb рейтинг фильма
    - **genre**: жанры фильма
    - **description**: описание фильма
    - **actors**: актёры
    - **writers**: сценаристы
    - **director**: режиссёры
    """
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.FILM_NOT_FOUND,
        )
    return film


@router.get(
    '/',
    response_model=list[Film],
    summary="Получить список фильмов",
)
async def film_list(
    film_list: list[Film] = Depends(service.get_film_list),
) -> list[Film]:
    """
    Получить список фильмов с полной информацией:

    - **id**: идентификатор
    - **title**: название фильма
    - **imdb_rating**: imdb рейтинг фильма
    - **genre**: жанры фильма
    - **description**: описание фильма
    - **actors**: актёры
    - **writers**: сценаристы
    - **director**: режиссёры
    """
    if not film_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.FILMS_NOT_FOUND,
        )
    return film_list
