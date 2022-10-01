import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Movie:
    id: uuid.UUID
    imdb_rating: float
    genre: list
    title: str
    description: str
    modified: datetime
    director: str
    actors_names: list
    writers_names: list
    actors: list
    writers: list

    def __post_init__(self):
        if self.imdb_rating is None:
            self.imdb_rating = 0.0
        if self.description is None:
            self.description = ''
        if self.director is None:
            self.director = ''
