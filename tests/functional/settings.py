from pydantic import BaseSettings, Field
from etl.src.schemas.elastic import ELASTIC_MAPPINGS, ELASTIC_MAPPINGS_ALL_GENRES, ELASTIC_MAPPINGS_ALL_PERSONS


class TestSettings(BaseSettings):
    es_host: str = Field(default='http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_index: str = Field(default='movies', env='PROJECT_NAME')
    es_id_field: str = 'eeeeeeeee'
    es_index_mapping: dict = ELASTIC_MAPPINGS

    redis_host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    service_url: int = Field(default=6379, env='REDIS_PORT')


test_settings = TestSettings()