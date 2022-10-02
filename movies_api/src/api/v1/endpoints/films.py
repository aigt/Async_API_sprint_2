from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

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


@router.get('/search', response_model=list[Film])
async def film_search(
    query_config: FilmListQueryConfig = Depends(film_search_query_config),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    return await film_list_by_query_config(
        query_config=query_config,
        film_service=film_service,
    )


@router.get('/{film_id}', response_model=Film)
@cached.cached_id_item(id_name='film_id')
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
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


@router.get('/', response_model=list[Film])
async def film_list(
    query_config: FilmListQueryConfig = Depends(film_list_query_config),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    return await film_list_by_query_config(
        query_config=query_config,
        film_service=film_service,
    )
