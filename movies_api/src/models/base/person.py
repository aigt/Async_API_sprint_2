import uuid

from models import film
from models.base import orjson_model


class Person(orjson_model.OrjsonModel):
    """Базовый класс для персон."""

    id: uuid.UUID
    full_name: str
    role: str
    films: list[film.Film]
