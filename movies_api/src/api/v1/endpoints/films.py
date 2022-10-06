import uuid as uuid_m
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.schemas import Film
from cache import cached
from core import text_messages
from dependencies.film_list_query_body import (film_list_query_body,
                                               film_search_query_body)
from services.film import FilmService, get_film_service

router = APIRouter()


async def film_list_by_query(
    query_body: dict,
    film_service: FilmService,
) -> list[Film]:
    films = await film_service.list(query_body=query_body)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.FILMS_NOT_FOUND,
        )

    return [
        Film(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            genre=film.genre,
            description=film.description,
            actors=film.actors,
            writers=film.writers,
            director=film.director,
        )
        for film in films
    ]


@router.get(
    '/search',
    response_model=list[Film],
    summary="Найти фильмы по запросу",
)
async def film_search(
    query_body: dict = Depends(film_search_query_body),
    film_service: FilmService = Depends(get_film_service),
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

    return await film_list_by_query(
        query_body=query_body,
        film_service=film_service,
    )


@router.get(
    '/{film_id}',
    response_model=Film,
    summary="Получить фильм",
)
@cached.cached_id_item(id_name='film_id')
async def film_details(
    film_id: uuid_m.UUID = Query(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым фильм хранится в БД",
    ),
    film_service: FilmService = Depends(get_film_service),
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
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.FILM_NOT_FOUND,
        )

    return Film(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        genre=film.genre,
        description=film.description,
        actors=film.actors,
        writers=film.writers,
        director=film.director,
    )


@router.get(
    '/',
    response_model=list[Film],
    summary="Получить список фильмов",
)
async def film_list(
    query_body: dict = Depends(film_list_query_body),
    film_service: FilmService = Depends(get_film_service),
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
    return await film_list_by_query(
        query_body=query_body,
        film_service=film_service,
    )
