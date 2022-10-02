import uuid

from models.base import orjson_model


class Person(orjson_model.OrjsonModel):
    id: uuid.UUID
    full_name: str
    role: list[str] | None
    film_ids: list[str] | None
