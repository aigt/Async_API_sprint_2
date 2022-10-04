import uuid

from models.base import orjson_model


class Genre(orjson_model.OrjsonModel):
    id: uuid.UUID
    name: str
