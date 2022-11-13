import uuid
from datetime import datetime

from pydantic import BaseModel, dataclass


class Person(BaseModel):
    id: uuid.UUID
    name: str

@dataclass
class Movie:
    id: uuid.UUID
    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: str
    actors_names: list[str]
    writers_names: list[str]
    actors: list[Person]
    writers: list[Person]
