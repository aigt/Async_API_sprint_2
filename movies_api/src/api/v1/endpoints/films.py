from http import HTTPStatus
import uuid as uuid_m

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.schemas import Film
from cache import cached
from core import text_messages
from dependencies.film_list_query_config import (
    film_list_query_config,
    film_search_query_config,
)
from models.es_query_configs.film_list_query_config import FilmListQueryConfig
from services.film import FilmService, get_film_service

router = APIRouter()


async def film_list_by_query_config(
    query_config: FilmListQueryConfig,
    film_service: FilmService,
) -> list[Film]:
    films = await film_service.list(query_config)
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
    query_config: FilmListQueryConfig = Depends(film_search_query_config),
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

    return await film_list_by_query_config(
        query_config=query_config,
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
    query_config: FilmListQueryConfig = Depends(film_list_query_config),
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
    return await film_list_by_query_config(
        query_config=query_config,
        film_service=film_service,
    )
