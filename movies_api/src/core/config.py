from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field, RedisDsn, validator

# Корень проекта
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):

    # Название проекта. Используется в Swagger-документации
    project_name: str = Field(default='movies', env='PROJECT_NAME')

    API_V1_STR: str = "/api/v1"

    # Настройки Redis
    redis_host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(default=6379, env='REDIS_PORT')

    redis_dsn: RedisDsn | None = None

    @validator('redis_dsn', pre=True)
    def create_redis_dsn(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme='redis',
            host=values.get('redis_host'),
            port=f'{values.get("redis_port")}',
        )

    # Настройки Elasticsearch
    elastic_host: str = Field(default='127.0.0.1', env='ELASTIC_HOST')
    elastic_port: int = Field(default=9200, env='ELASTIC_PORT')

    # Максимальное количество элементов на странице
    max_page_size: int = Field(default=50)


@lru_cache()
def get_settings():
    return Settings()
