from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field, RedisDsn, validator


class Settings(BaseSettings):

    # Название проекта. Используется в Swagger-документации
    project_name: str = Field(default='movies', env='PROJECT_NAME')

    API_V1_STR: str = "/api/v1"

    # Настройки Redis
    CACHE_EXPIRE_IN_SECONDS = 60 * 5

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
    
    # Публичный ключ для декодирования токенов авторизации
    auth_rsa_public_key = Field(default='')
    
    # Роль в токене, по которой идентифицируется подписчик
    subscriber_role_name = 'subscriber'

    # Адрес для логирования ошибок
    sentry_dsn: str = "https://4d3cd8b5585e41fda8dc722e72ca93a8@o4504286904188928.ingest.sentry.io/4504287423561728"


@lru_cache()
def get_settings():
    return Settings()
