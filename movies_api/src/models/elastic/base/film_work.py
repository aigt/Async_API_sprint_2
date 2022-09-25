from __future__ import annotations

import uuid
from typing import List

from models.elastic.base import orjson_model


class FilmWork(orjson_model.OrjsonModel):
    """Базовый класс для кинопроизведений."""

    id: uuid.UUID
    imdb_rating: float
    title: str
    genre: List[str]
    description: str | None
    actors_names: List[str] | None
    writers_names: List[str] | None
    actors: List[actor.Actor]
    writers: List[writer.Writer]
    director: str


# Чтобы не было циклического импорта
from models.elastic import actor, director, writer  # noqa: E402, F401

FilmWork.update_forward_refs()
