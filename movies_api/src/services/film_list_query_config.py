import uuid

from fastapi import Depends, Query
from pydantic import BaseModel

from core import config


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


class BoolConfig(BaseModel):
    """Конфигурация комбинации списка фильмов."""

    filter: FilterConfig | None = None
    query: str | None = None


class FilmListQueryConfig(BaseModel):
    """Конфигурация запроса списка фильмов."""

    bool_q: BoolConfig | None = None
    page: PageConfig = PageConfig()
    sort: SortConfig | None = None


async def film_list_query_config(
    page_size: int | None = Query(default=None, alias="page[size]"),
    page_number: int | None = Query(default=None, alias="page[number]"),
    sort: str | None = Query(default=None),
    filter_genre: str | None = Query(default=None, alias="filter[genre]"),
) -> FilmListQueryConfig:

    query_config = FilmListQueryConfig()

    # Параметры пагинации
    if page_size is not None:
        if page_size > config.MAX_PAGE_SIZE:
            page_size = config.MAX_PAGE_SIZE
        query_config.page.size = page_size

    if page_number is not None:
        query_config.page.number = page_number

    # Параметры сортировки
    if sort is not None:
        query_config.sort = SortConfig()
        sort_key = sort
        if sort_key.startswith('-'):
            query_config.sort.order = 'desc'
            sort_key = sort_key[1:]
        query_config.sort.field = sort_key

    # Параметры фильтрации
    if filter_genre is not None:
        if query_config.bool_q is None:
            query_config.bool_q = BoolConfig()
        query_config.bool_q.filter = FilterConfig()
        query_config.bool_q.filter.field = 'genre'
        query_config.bool_q.filter.value = filter_genre

    return query_config


def film_search_query_config(
    query: str = Query(...),
    list_config: FilmListQueryConfig = Depends(film_list_query_config),
) -> FilmListQueryConfig:
    if list_config.bool_q is None:
        list_config.bool_q = BoolConfig()

    list_config.bool_q.query = query

    return list_config
