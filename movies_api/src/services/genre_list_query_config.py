import uuid
from typing import List

from core import config
from fastapi import Depends
from models.request.param_with_option import ParamWithOption
from pydantic import BaseModel
from services.query_params_with_option import get_params_with_options


class PageConfig(BaseModel):
    """Конфигурация пагинации списка жанров."""
    size: int = 20
    number: int = 1



class GenreListQueryConfig(BaseModel):
    """Конфигурация запроса списка жанров."""
    page: PageConfig = PageConfig()


async def genre_list_query_config(
    query_params: List[ParamWithOption] = Depends(get_params_with_options),
) -> GenreListQueryConfig:

    query_config = GenreListQueryConfig()

    for param in query_params:
        match param:
            # Параметры пагинации
            case ParamWithOption(name='page', option='size'):
                page_size = int(param.value)
                if page_size > config.MAX_PAGE_SIZE:
                    page_size = config.MAX_PAGE_SIZE
                query_config.page.size = int(param.value)

            case ParamWithOption(name='page', option='number'):
                query_config.page.number = int(param.value)

    return query_config
