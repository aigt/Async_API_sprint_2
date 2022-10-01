import uuid

from models.base import orjson_model


class Person(orjson_model.OrjsonModel):
    """Базовый класс для персон."""

    id: uuid.UUID
    name: str
