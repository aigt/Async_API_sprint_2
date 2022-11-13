import logging
import uuid as uuid_m

from api.v1.schemas import Film
from cache import cached
from core.text_messages import FURTHER_INFORMATION_ONLY_FOR_SUBSCRIBERS
from fastapi import Depends, Path
from models.elastic.film import Film as ElasticFilm
from repositories.elastic import ElastisearchRepository, get_film_repository
from services.film.film_list_query_body import (film_list_query_body,
                                                film_search_query_body)
from services.jwt import is_subscriber


def _map_film(film: ElasticFilm, user_is_subscriber: bool) -> Film:
    """Маппинг схемы фильма индекса ES к схеме API.

    Args:
        film (ElasticFilm): фильм из индекса ES
        is_subscriber (bool): Запрос на отображение от подписчика

    Returns:
        Film: фильм индекса API
    """
    if film.subscription and not user_is_subscriber:
        return Film(
            id=film.id,
            title=film.title,
            imdb_rating=0,
            genre=[],
            description=FURTHER_INFORMATION_ONLY_FOR_SUBSCRIBERS,
            actors=[],
            writers=[],
            director='',
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


async def _film_list_by_query(
    query_body: dict,
    film_repo: ElastisearchRepository[ElasticFilm],
    user_is_subscriber: bool,
) -> list[Film]:
    films = await film_repo.list(query_body=query_body)
    return [_map_film(film, user_is_subscriber) for film in films]


async def get_film_list(
    query_body: dict = Depends(film_list_query_body),
    film_repo: ElastisearchRepository[ElasticFilm] = Depends(get_film_repository),
    user_is_subscriber: bool = Depends(is_subscriber),
) -> list[Film]:
    return await _film_list_by_query(
        query_body=query_body,
        film_repo=film_repo,
        user_is_subscriber=user_is_subscriber,
    )


async def search_films(
    query_body: dict = Depends(film_search_query_body),
    film_repo: ElastisearchRepository[ElasticFilm] = Depends(get_film_repository),
    user_is_subscriber: bool = Depends(is_subscriber),
) -> list[Film]:
    return await _film_list_by_query(
        query_body=query_body,
        film_repo=film_repo,
        user_is_subscriber=user_is_subscriber,
    )


@cached.cached_id_item(id_name='film_id')
async def get_film_by_id(
    film_id: uuid_m.UUID = Path(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым фильм хранится в БД",
    ),
    film_repo: ElastisearchRepository[ElasticFilm] = Depends(get_film_repository),
    user_is_subscriber: bool = Depends(is_subscriber),
) -> Film | None:
    film = await film_repo.get_by_id(film_id)
    if not film:
        return None
    return _map_film(film, user_is_subscriber)
