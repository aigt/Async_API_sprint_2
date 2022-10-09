import uuid
from datetime import datetime

from pydantic import BaseModel, validator


class Role(BaseModel):
    role: str
    film_id: uuid.UUID
    film_title: str
    film_imdb_rating: float | None
    
    @validator('film_imdb_rating')
    def set_film_imdb_rating(cls, film_imdb_rating):
        return film_imdb_rating or 0.0

class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    modified: datetime
    roles: list[Role]
