import os
from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
    PostgresDsn,
    PyObject,
    RedisDsn,
    validator,
)

ELASTIC_PATH = os.getenv("ELASTIC_PATH")


MOVIES_STATE_PATH = "save_movie_state.json"
GENRES_STATE_PATH = "save_genre_state.json"
PERSONS_STATE_PATH = "save_person_state.json"
ALL_GENRES_STATE_PATH = 'save_all_genres_state.json'
ALL_PERSONS_STATE_PATH = 'save_all_persons_state.json'


ELASTIC_SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {"type": "stemmer", "language": "english"},
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {"type": "stemmer", "language": "russian"},
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}


ELASTIC_MAPPINGS = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "imdb_rating": {"type": "float"},
        "genre": {"type": "keyword"},
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {"raw": {"type": "keyword"}},
        },
        "description": {"type": "text", "analyzer": "ru_en"},
        "director": {"type": "text", "analyzer": "ru_en"},
        "actors_names": {"type": "text", "analyzer": "ru_en"},
        "writers_names": {"type": "text", "analyzer": "ru_en"},
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

ELASTIC_MAPPINGS_ALL_GENRES = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "name": {"type": "text"},
    },
}

ELASTIC_MAPPINGS_ALL_PERSONS = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "full_name": {"type": "text"},
    },
}

ALL_MAPPINGS = {
    "movies": ELASTIC_MAPPINGS,
    "genres": ELASTIC_MAPPINGS_ALL_GENRES,
    "persons": ELASTIC_MAPPINGS_ALL_PERSONS,
}


ELASTIC_INDEX = {"movies": "movies", "genres": "genres", "persons": "persons"}


class Settings(BaseSettings):

    # PostgreSQL database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_NAME: str
    POSTGRES_PORT: int
    POSTGRES_DSN: Optional[PostgresDsn] = None

    @validator('POSTGRES_DSN', pre=True)
    def create_postgres_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_NAME') or ''}",
            port=f"{values.get('POSTGRES_PORT')}",
        )

    class Config:
        case_sensitive = True


@lru_cache()
def get_pg_settings():
    return Settings()
