import orjson
import uuid

from pydantic import BaseModel
from typing import List


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    # с role непонятно - роль привязана к конкретному фильму
    # role: str
    # film_ids: List[uuid.UUID]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
