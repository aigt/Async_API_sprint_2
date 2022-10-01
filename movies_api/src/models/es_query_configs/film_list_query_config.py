import uuid

from pydantic import BaseModel


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
