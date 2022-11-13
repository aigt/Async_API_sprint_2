import asyncio
import logging.config
import time

import uvloop

from core.config import get_settings
from core.logger import LOGGING
from operations.extract import PostgresExtractor
from operations.load import ElasticLoader
from operations.transform import DataTransformer
from schemas import elastic as es_schemas
from sql.sql import extract_queries
from states.state import JsonFileStorage, State

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# Применяем настройки логирования
logging.config.dictConfig(LOGGING)

settings = get_settings()


def etl(
    extractor: PostgresExtractor, transformer: DataTransformer, loader: ElasticLoader
) -> None:
    """Функция для последовательного запуска экземпляров ETL-процесса"""
    logging.info("ETL process was started.")
    data = extractor.extract()
    transformed_data = transformer.transform(data)
    loader.load(transformed_data)


if __name__ == "__main__":

    states = {
        "movie": State(
            storage=JsonFileStorage(file_path=settings.MOVIES_STATE_PATH),
        ),
        "genre": State(
            storage=JsonFileStorage(file_path=settings.GENRES_STATE_PATH),
        ),
        "person": State(
            storage=JsonFileStorage(file_path=settings.PERSONS_STATE_PATH),
        ),
        "all_genres": State(
            storage=JsonFileStorage(file_path=settings.ALL_GENRES_STATE_PATH),
        ),
        "all_persons": State(
            storage=JsonFileStorage(file_path=settings.ALL_PERSONS_STATE_PATH),
        ),
    }

    movies_extractor = PostgresExtractor(
        dsn=settings.POSTGRES_DSN, query=extract_queries, state=states
    )
    movies_transformer = DataTransformer()
    movies_loader = ElasticLoader(
        conn=settings.ELASTIC_PATH,
        index=es_schemas.ELASTIC_INDEX,
        settings=es_schemas.ELASTIC_SETTINGS,
        mappings=es_schemas.ALL_MAPPINGS,
        state=states,
    )
    while True:
        etl(
            extractor=movies_extractor,
            transformer=movies_transformer,
            loader=movies_loader,
        )
        time.sleep(60 * 10)
