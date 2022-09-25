import uuid
from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.film import FilmService, get_film_service
from services.film_list_query_config import FilmListQueryConfig, film_list_query_config

router = APIRouter()


class Film(BaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float
    genre: List[Any]
    description: str
    actors: List[Any]
    writers: List[Any]
    director: str


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус.
        # Желательно пользоваться уже определёнными HTTP-статусами, которые
        # содержат enum.
        # Такой код будет более поддерживаемым.
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='film not found',
        )

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description
    # Которое отсутствует в модели ответа API.
    # Если бы использовалась общая модель для бизнес-логики и формирования
    # ответов API
    # вы бы предоставляли клиентам данные, которые им не нужны
    # и, возможно, данные, которые опасно возвращать
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


class SBrac(BaseModel):
    filter: List[dict]


@router.get('/')  # , response_model=List[Film])
async def film_list(
    query_config: FilmListQueryConfig = Depends(film_list_query_config),
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:

    films = await film_service.list(query_config)
    # logging.info(films)

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='any film is not found',
        )

    return {
        'films': [
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
    }
