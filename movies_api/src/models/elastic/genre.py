import uuid

from models.elastic.base import orjson_model


class Genre(orjson_model.OrjsonModel):
    """Жанр."""

    id: uuid.UUID
    name: str
    age_limit: int
