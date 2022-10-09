import uuid

from models.base import orjson_model


class Role(orjson_model.OrjsonModel):
    role: str
    film_id: uuid.UUID
    film_title: str
    film_imdb_rating: float

class Person(orjson_model.OrjsonModel):
    id: uuid.UUID
    full_name: str
    roles: list[Role]