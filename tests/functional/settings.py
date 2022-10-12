from functools import lru_cache

from pydantic import BaseSettings, Field

from testdata.schemas import (ES_GENRES_MAP, ES_INDEXES, ES_MOVIES_MAP,
                               ES_PERSONS_MAP)


class TestSettings(BaseSettings):
    es_host: str = Field(default='http://127.0.0.1:9200', env='ELASTIC_URL')
    es_index: dict = ES_INDEXES
    es_id_field: str = 'title'
    es_index_mapping: dict = ES_MOVIES_MAP

    redis_host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    service_url: str = Field(default='http://127.0.0.1:8000', env='SERVICE_URL')


@lru_cache
def get_settings():
    return TestSettings()