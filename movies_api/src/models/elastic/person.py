import uuid
from typing import List

from models.base import orjson_model


class Person(orjson_model.OrjsonModel):
    id: uuid.UUID
    full_name: str
    role: List[str] | None
    film_ids: List[str] | None
