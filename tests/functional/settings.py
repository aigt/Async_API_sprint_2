from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field, RedisDsn, validator

from testdata.schemas import ES_INDEXES, ES_MOVIES_MAP


class TestSettings(BaseSettings):
    es_host: str = Field(default='http://127.0.0.1:9200', env='ELASTIC_URL')
    es_index: dict = ES_INDEXES
    es_id_field: str = 'title'
    es_index_mapping: dict = ES_MOVIES_MAP

    redis_host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    service_url: str = Field(default='http://127.0.0.1:8000', env='SERVICE_URL')
    
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


@lru_cache
def get_settings():
    return TestSettings()