import logging
import re
import uuid
from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from models.request.param_with_option import ParamWithOption
from services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    id: uuid.UUID
    title: str


def parse_param(param: str, value: Any) -> ParamWithOption:
    """Функция для поддержки квадратных скобок в имени переменных запроса.

    Args:
        param (str): Имя параметра
        value (Any): Переменная

    Returns:
        ParamWithOption: объект параметра с опцией
    """
    regex = r"(?P<param>.*)\[(?P<option>.*)\]"
    if m := re.search(regex, param):
        return ParamWithOption(
            name=m.group("param"),
            option=m.group("option"),
            value=value,
        )
    return ParamWithOption(name=param, value=value)


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
    return Film(id=film.id, title=film.title)


class SBrac(BaseModel):
    filter: List[dict]


@router.get('/')  # , response_model=List[Film])
async def film_list(
    request: Request,
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:

    qs = [parse_param(k, v) for k, v in request.query_params.items()]
    logging.info(f'{qs=}')

    films = await film_service.list(qs)
    logging.info(films)

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='any film is not found',
        )

    return {'films': [Film(id=film.id, title=film.title) for film in films]}
