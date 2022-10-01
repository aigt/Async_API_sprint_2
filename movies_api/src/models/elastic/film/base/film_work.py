from __future__ import annotations

import uuid

from pydantic import validator

from models.base import orjson_model


class FilmWork(orjson_model.OrjsonModel):
    """Базовый класс для кинопроизведений."""

    id: uuid.UUID
    imdb_rating: float | None
    title: str
    genre: list[str]
    description: str | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    actors: list[actor.Actor]
    writers: list[writer.Writer]
    director: str

    @validator('description')
    def set_description(cls, description):
        return description or ''

    @validator('imdb_rating')
    def set_imdb_rating(cls, imdb_rating):
        return imdb_rating or 0.0


# Чтобы не было циклического импорта
from models.elastic.film import actor, writer  # noqa: E402, F401

FilmWork.update_forward_refs()
