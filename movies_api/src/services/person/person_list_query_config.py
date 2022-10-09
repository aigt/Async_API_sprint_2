from fastapi import Depends, Query

from core.config import get_settings
from models.es_query_configs.person_list_query_config import (
    BoolConfig, PersonListQueryConfig)

settings = get_settings()


async def person_list_query_config(
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
) -> PersonListQueryConfig:

    query_config = PersonListQueryConfig()

    # Параметры пагинации
    if page_size is not None:
        if page_size > settings.max_page_size:
            page_size = settings.max_page_size
        query_config.page.size = page_size

    if page_number is not None:
        query_config.page.number = page_number

    return query_config


async def person_search_query_config(
    query: str = Query(
        ...,
        title="Запрос",
        description="Запрос, по которому осуществляется поиск",
    ),
    list_config: PersonListQueryConfig = Depends(person_list_query_config),
) -> PersonListQueryConfig:
    if list_config.bool_q is None:
        list_config.bool_q = BoolConfig()

    list_config.bool_q.query = query

    return list_config
