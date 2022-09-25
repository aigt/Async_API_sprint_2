import uuid

from models.elastic.base import film_work, orjson_model


class Person(orjson_model.OrjsonModel):
    """Базовый класс для персон."""

    id: uuid.UUID
    name: str
    # full_name: str
    # role: str
    # films: list[film_work.FilmWork]
