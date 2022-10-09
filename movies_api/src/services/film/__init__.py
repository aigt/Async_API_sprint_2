import uuid as uuid_m

from fastapi import Depends, Path

from api.v1.schemas import Film
from cache import cached
from repositories.elastic import ElastisearchRepository, get_film_repository
from services.film.film_list_query_body import (film_list_query_body,
                                                film_search_query_body)


async def _film_list_by_query(
    query_body: dict,
    film_repo: ElastisearchRepository,
) -> list[Film]:
    films = await film_repo.list(query_body=query_body)
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


async def get_film_list(
    query_body: dict = Depends(film_list_query_body),
    film_repo: ElastisearchRepository = Depends(get_film_repository),
) -> list[Film]:
    return await _film_list_by_query(
        query_body=query_body,
        film_repo=film_repo,
    )


async def search_films(
    query_body: dict = Depends(film_search_query_body),
    film_repo: ElastisearchRepository = Depends(get_film_repository),
) -> list[Film]:
    return await _film_list_by_query(
        query_body=query_body,
        film_repo=film_repo,
    )


@cached.cached_id_item(id_name='film_id')
async def get_film_by_id(
    film_id: uuid_m.UUID = Path(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым фильм хранится в БД",
    ),
    film_repo: ElastisearchRepository = Depends(get_film_repository),
) -> Film | None:
    film = await film_repo.get_by_id(film_id)
    if not film:
        return None
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
