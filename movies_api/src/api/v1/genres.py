import uuid

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from services.genre import GenreService, get_genre_service
from services.film_list_query_config import FilmListQueryConfig, film_list_query_config


router = APIRouter()


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str,
                        genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return Genre(uuid=genre.id, name=genre.name)


@router.get('/')
async def genres_list(
    query_config: FilmListQueryConfig = Depends(film_list_query_config),
    genre_service: GenreService = Depends(get_genre_service),
) -> List[Genre]:

    genres = await genre_service.list(query_config)

    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='genres not found',
        )

    return [Genre(uuid=genre.id, name=genre.name,) for genre in genres]
