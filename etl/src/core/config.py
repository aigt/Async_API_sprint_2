from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):

    MOVIES_STATE_PATH = "save_movie_state.json"
    GENRES_STATE_PATH = "save_genre_state.json"
    PERSONS_STATE_PATH = "save_person_state.json"
    ALL_GENRES_STATE_PATH = 'save_all_genres_state.json'
    ALL_PERSONS_STATE_PATH = 'save_all_persons_state.json'

    # Elasticsearch settings
    ELASTIC_PATH: str = 'http://127.0.0.1:9200'

    # PostgreSQL database settings
    POSTGRES_USER: str = 'app'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_NAME: str = 'postgres'
    POSTGRES_PORT: int = 5432
    POSTGRES_DSN: PostgresDsn | None = None

    @validator('POSTGRES_DSN', pre=True)
    def create_postgres_uri(cls, v: str | None, values: dict[str, Any]) -> Any:
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
def get_settings():
    return Settings()
