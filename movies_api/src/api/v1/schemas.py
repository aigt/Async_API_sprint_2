import uuid as uuid_m

from pydantic import BaseModel, Field


class FilmPerson(BaseModel):
    """Персоны для схемы Film."""

    id: uuid_m.UUID = Field(
        title='Идентификатор',
        description='Идентификатор под которым персона хранится в БД',
    )
    name: str = Field(
        title='Имя',
        description='Полние имя персоны',
    )


class Film(BaseModel):
    """Схема возвращаемого фильма."""

    id: uuid_m.UUID = Field(
        title='Идентификатор',
        description='Идентификатор под которым фильм хранится в БД',
    )
    title: str = Field(
        title='Название фильма',
        description='Официальное название фильма',
    )
    imdb_rating: float = Field(
        title='IMDb рейтинг фильма',
        description='Рейтинг фильма с сайта Internet Movie Database (IMDb)',
    )
    genre: list[str] = Field(
        title='Жанры фильма',
        description='Список жанров к которым относится фильм',
    )
    description: str = Field(
        title='Описание фильма',
        description='Описание фильма',
    )
    actors: list[FilmPerson] = Field(
        title='Актёры',
        description='Актёры снимавшиеся в фильме',
    )
    writers: list[FilmPerson] = Field(
        title='Сценаристы',
        description='Сценаристы, принимавшие участие в написании сценария для данного фильма',
    )
    director: str = Field(
        title='Режиссёр',
        description='Режиссёр этого фильма',
    )


class Genre(BaseModel):
    """Схема возвращаемого жанра."""

    uuid: uuid_m.UUID = Field(
        title='Идентификатор',
        description='Идентификатор под которым жанр хранится в БД',
    )
    name: str = Field(
        title='Название',
        description='Название жанра',
    )


class Person(BaseModel):
    """Схема возвращаемой персоны."""

    uuid: uuid_m.UUID = Field(
        title='Идентификатор',
        description='Идентификатор под которым персона хранится в БД',
    )
    full_name: str = Field(
        title='Полние имя персоны',
        description='Полние имя персоны',
    )
    film_ids: list[uuid_m.UUID] | None = Field(
        title='Идентификаторы фильмов',
        description='Список идентификаторов фильмов, в которых персона принимала участие',
    )
    role: list[str] | None = Field(
        title='Список должностей',
        description='Список должностей, которые занимала данная персона',
    )
