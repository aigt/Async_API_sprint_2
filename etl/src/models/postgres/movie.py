import uuid
from datetime import datetime

from pydantic import BaseModel, validator


class Person(BaseModel):
    id: uuid.UUID
    name: str


class Movie(BaseModel):
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
    modified: datetime

    @validator('imdb_rating')
    def set_imdb_rating(cls, imdb_rating):
        return imdb_rating or 0.0
    
    @validator('description')
    def set_description(cls, description):
        return description or ''
    
    @validator('director')
    def set_description(cls, director):
        return director or ''
