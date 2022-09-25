from __future__ import annotations

import uuid
from typing import List

from models.elastic.base import orjson_model
from pydantic import validator


class FilmWork(orjson_model.OrjsonModel):
    """Базовый класс для кинопроизведений."""

    id: uuid.UUID
    imdb_rating: float | None
    title: str
    genre: List[str]
    description: str | None
    actors_names: List[str] | None
    writers_names: List[str] | None
    actors: List[actor.Actor]
    writers: List[writer.Writer]
    director: str

    @validator('description')
    def set_description(cls, description):
        return description or ''

    @validator('imdb_rating')
    def set_imdb_rating(cls, imdb_rating):
        return imdb_rating or 0.0


# Чтобы не было циклического импорта
from models.elastic import actor, director, writer  # noqa: E402, F401

FilmWork.update_forward_refs()
