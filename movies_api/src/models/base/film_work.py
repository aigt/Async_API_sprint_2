import datetime
import uuid

from models import actor, director, writer
from models.base import orjson_model


class FilmWork(orjson_model.OrjsonModel):
    """Базовый класс для кинопроизведений."""

    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    genre: list[str]
    actors: list[actor.Actor]
    writers: list[writer.Writer]
    directors: list[director.Director]
    file_link: str
