from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas import Genre
from core import text_messages
from core.config import get_settings
from services import genre as service

router = APIRouter()

settings = get_settings()


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Получить жанр",
)
async def get_genre_by_id(
    genre: Genre | None = Depends(service.get_genre_by_id),
) -> Genre:
    """
    Получить жанр с полной информацией:

    - **id**: идентификатор
    - **name**: название жанра
    """
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.GENRE_NOT_FOUND,
        )
    return genre


@router.get(
    "/",
    response_model=list[Genre],
    summary="Получить список жанров",
)
async def genres_list(
    genre_list: list[Genre] = Depends(service.get_genre_list),
) -> list[Genre]:
    """
    Получить список жанров с полной информацией:

    - **id**: идентификатор
    - **name**: название жанра
    """
    if not genre_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.GENRES_NOT_FOUND,
        )
    return genre_list
