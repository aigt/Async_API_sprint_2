import uuid
from typing import Any

from pydantic import BaseModel


class Film(BaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float
    genre: list[Any]
    description: str
    actors: list[Any]
    writers: list[Any]
    director: str


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    film_ids: list | None
    role: list | None
