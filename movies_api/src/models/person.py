import orjson
import uuid

from pydantic import BaseModel
from typing import List


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    role: List[str] | None
    film_ids: List[str] | None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
