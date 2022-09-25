import uuid
from typing import List

from fastapi import Depends
from pydantic import BaseModel

from models.request.param_with_option import ParamWithOption
from services.query_params_with_option import get_params_with_options


class PageConfig(BaseModel):
    size: int = 20
    number: int = 0


class FilterConfig(BaseModel):
    field: str | None = None
    value: uuid.UUID | None = None


class FilmListQueryConfig(BaseModel):
    page: PageConfig = PageConfig()
    filter: FilterConfig = FilterConfig()
    sort: str | None = None


async def film_list_query_config(
    query_params: List[ParamWithOption] = Depends(get_params_with_options),
) -> FilmListQueryConfig:

    query_config = FilmListQueryConfig()

    for param in query_params:
        match param:
            case ParamWithOption(name='sort'):
                query_config.sort = param.value
            case ParamWithOption(name='page', option='size'):
                query_config.page.size = param.value
            case ParamWithOption(name='page', option='number'):
                query_config.page.number = param.value
            case ParamWithOption(name='filter'):
                query_config.filter.field = param.option
                query_config.filter.value = param.value

    return query_config
