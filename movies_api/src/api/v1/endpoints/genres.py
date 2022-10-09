from http import HTTPStatus
import uuid as uuid_m

from fastapi import APIRouter, Depends, HTTPException, Query, Path

from api.v1.schemas import Genre
from cache import cached
from core import text_messages
from core.config import get_settings
from services.genre import GenreService, get_genre_service

router = APIRouter()

settings = get_settings()


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Получить жанр",
)
@cached.cached_id_item(id_name='genre_id')
async def genre_details(
    genre_id: uuid_m.UUID = Path(
        ...,
        title="Идентификатор",
        description="Идентификатор под которым жанр хранится в БД",
    ),
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    """
    Получить жанр с полной информацией:

    - **id**: идентификатор
    - **name**: название жанра
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.GENRE_NOT_FOUND,
        )
    return Genre(
        uuid=genre.id,
        name=genre.name,
    )


@router.get(
    "/",
    response_model=list[Genre],
    summary="Получить список жанров",
)
async def genres_list(
    page_size: int = Query(
        default=20,
        alias="page[size]",
        title="Размер списка",
        description="Количество элементов выдаваемых на одной странице",
        le=settings.max_page_size,
    ),
    page_number: int = Query(
        default=1,
        alias="page[number]",
        title="Номер страницы",
        description="Номер страницы, которую загрузить",
    ),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    """
    Получить список жанров с полной информацией:

    - **id**: идентификатор
    - **name**: название жанра
    """
    genres = await genre_service.list(page_number, page_size)

    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=text_messages.GENRES_NOT_FOUND,
        )
    return [
        Genre(
            uuid=genre.id,
            name=genre.name,
        )
        for genre in genres
    ]
