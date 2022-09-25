import uuid
from typing import List

from fastapi import Depends
from pydantic import BaseModel

from core import config
from models.request.param_with_option import ParamWithOption
from services.query_params_with_option import get_params_with_options


class PageConfig(BaseModel):
    """Конфигурация пагинации списка фильмов."""

    size: int = 20
    number: int = 1


class FilterConfig(BaseModel):
    """Конфигурация фильтрации списка фильмов."""

    field: str | None = None
    value: uuid.UUID | None = None


class SortConfig(BaseModel):
    """Конфигурация сортировки списка фильмов."""

    field: str | None = None
    order: str = 'asc'


class FilmListQueryConfig(BaseModel):
    """Конфигурация запроса списка фильмов."""

    filter: FilterConfig = None
    page: PageConfig = PageConfig()
    sort: SortConfig | None = None


async def film_list_query_config(
    query_params: List[ParamWithOption] = Depends(get_params_with_options),
) -> FilmListQueryConfig:

    query_config = FilmListQueryConfig()

    for param in query_params:
        match param:
            # Параметры сортировки
            case ParamWithOption(name='sort'):
                query_config.sort = SortConfig()
                sort_key = param.value
                if sort_key.startswith('-'):
                    query_config.sort.order = 'desc'
                    sort_key = sort_key[1:]
                query_config.sort.field = sort_key

            # Параметры пагинации
            case ParamWithOption(name='page', option='size'):
                page_size = int(param.value)
                if page_size > config.MAX_PAGE_SIZE:
                    page_size = config.MAX_PAGE_SIZE
                query_config.page.size = int(param.value)

            case ParamWithOption(name='page', option='number'):
                query_config.page.number = int(param.value)

            # Параметры фильтрации
            case ParamWithOption(name='filter'):
                query_config.filter = FilterConfig()
                query_config.filter.field = param.option
                query_config.filter.value = param.value

    return query_config
