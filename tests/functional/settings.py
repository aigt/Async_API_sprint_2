from pydantic import BaseSettings, Field
from tests.functional.testdata.schemas import ES_MOVIES_MAP, ES_PERSONS_MAP, ES_GENRES_MAP


class TestSettings(BaseSettings):
    es_host: str = Field(default='http://127.0.0.1:9200', env='ELASTIC_URL')
    es_index: str = 'movies'
    es_id_field: str = 'title'
    es_index_mapping: dict = ES_MOVIES_MAP

    redis_host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    service_url: str = Field(default='http://127.0.0.1:8000', env='SERVICE_URL')


test_settings = TestSettings()