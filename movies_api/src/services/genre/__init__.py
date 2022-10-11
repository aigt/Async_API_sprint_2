import uuid as uuid_m

from fastapi import Depends, Path

from api.v1.schemas import Genre
from cache import cached
from models.elastic.genre import Genre as ElasticGenre
from repositories.elastic import ElastisearchRepository, get_genre_repository
from services.genre.genre_list_query_body import genre_list_query_body


def _map_genre(genre: ElasticGenre) -> Genre:
    """Маппинг схемы жанра индекса ES к схеме API.

    Args:
        genre (ElasticGenre): жанр из индекса ES

    Returns:
        Genre: жанр индекса API
    """
    return Genre(
        uuid=genre.id,
        name=genre.name,
    )


async def get_genre_list(
    query_body: dict = Depends(genre_list_query_body),
    genre_repo: ElastisearchRepository[ElasticGenre] = Depends(get_genre_repository),
) -> list[Genre]:
    genres = await genre_repo.list(query_body=query_body)
    return [_map_genre(genre) for genre in genres]


@cached.cached_id_item(id_name='genre_id')
async def get_genre_by_id(
    genre_id: uuid_m.UUID = Path(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым фильм хранится в БД",
    ),
    genre_repo: ElastisearchRepository[ElasticGenre] = Depends(get_genre_repository),
) -> Genre | None:
    genre = await genre_repo.get_by_id(genre_id)
    if not genre:
        return None
    return _map_genre(genre)