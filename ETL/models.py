import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Movie:
    id: uuid.UUID
    imdb_rating: float | None
    genre: list
    title: str
    description: str | None
    modified: datetime
    director: str | None
    actors_names: list
    writers_names: list
    actors: list
    writers: list


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    modified: datetime
