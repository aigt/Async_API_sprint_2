from fastapi import Query

from core.config import get_settings
from models.es_query_configs.film_list_query_config import FilmListQueryConfig
from services.film.film_list_query_config import (film_list_query_config,
                                                  film_search_query_config)

settings = get_settings()


async def _build_genre_list_es_query_body(page_number: int, page_size: int) -> dict:
    body = {
        'size': page_size,
        'from': (page_number - 1) * page_size,
        'query': {'match_all': {}},
    }

    return body


async def genre_list_query_body(
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
        ge=1,
    ),
) -> dict:
    return await _build_genre_list_es_query_body(page_number, page_size)
