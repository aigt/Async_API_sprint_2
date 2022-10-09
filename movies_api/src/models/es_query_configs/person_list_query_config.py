from pydantic import BaseModel


class PageConfig(BaseModel):
    """Конфигурация пагинации списка персон."""

    size: int = 20
    number: int = 1


class BoolConfig(BaseModel):
    """Конфигурация комбинации списка парсон."""

    query: str | None = None


class PersonListQueryConfig(BaseModel):
    """Конфигурация запроса списка персон."""

    bool_q: BoolConfig | None = None
    page: PageConfig = PageConfig()
