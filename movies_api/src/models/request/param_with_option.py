from typing import Any

from pydantic import BaseModel


class ParamWithOption(BaseModel):
    """Объект параметра с опцией.

    Например, в адресе запроса:
    /api/v1/films/?filter[genres]=horror&page[size]=50&sort=-imdb_rating

    будут 3 параметра:
            1       2       3
    name:   filter  page    sort
    option: genres  size    None
    value:  horror  50      -imdb_rating
    """

    name: str
    option: str | None
    value: Any | None
