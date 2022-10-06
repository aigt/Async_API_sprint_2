from fastapi import Depends, Query

from core.config import get_settings
from models.es_query_configs.film_list_query_config import (
    BoolConfig, FilmListQueryConfig, FilterConfig, SortConfig)

settings = get_settings()


async def film_list_query_config(
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
    sort: str
    | None = Query(
        default=None,
        title="Поле для сортировки",
        description="Поле для сортировки, для сортировки по возрастанию поле должно быть со знаком минус, например: -imdb_rating. На данный момент поддерживаетс сортировка только по полю imdb_rating.",
        regex='^-?imdb_rating$',
    ),
    filter_genre: str
    | None = Query(
        default=None,
        alias="filter[genre]",
        title="Фильтрация по определённому жанру",
        description="В списке останутся фильмы только с указанным жанром, например Fantasy.",
    ),
) -> FilmListQueryConfig:

    query_config = FilmListQueryConfig()

    # Параметры пагинации
    if page_size is not None:
        if page_size > settings.max_page_size:
            page_size = settings.max_page_size
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


async def film_search_query_config(
    query: str = Query(
        ...,
        title="Запрос",
        description="Запрос, по которому осуществляется поиск",
    ),
    list_config: FilmListQueryConfig = Depends(film_list_query_config),
) -> FilmListQueryConfig:
    if list_config.bool_q is None:
        list_config.bool_q = BoolConfig()

    list_config.bool_q.query = query

    return list_config
