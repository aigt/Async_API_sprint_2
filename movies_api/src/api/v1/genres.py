import uuid
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from cache import cached
from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str


@router.get("/{genre_id}", response_model=Genre)
@cached.cached_id_item(id_name='genre_id')
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return Genre(
        uuid=genre.id,
        name=genre.name,
    )


@router.get("/")
async def genres_list(
    genre_service: GenreService = Depends(get_genre_service),
    page_size: str | None = Query(default=None, alias="page[size]"),
    page_number: str | None = Query(default=None, alias="page[number]"),
) -> List[Genre]:
    genres = await genre_service.list(page_number, page_size)

    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="genres not found",
        )
    return [
        Genre(
            uuid=genre.id,
            name=genre.name,
        )
        for genre in genres
    ]
