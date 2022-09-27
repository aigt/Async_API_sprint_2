import logging.config

from core.config import (
    ALL_GENRES_STATE_PATH,
    ALL_MAPPINGS,
    ALL_PERSONS_STATE_PATH,
    ELASTIC_INDEX,
    ELASTIC_PATH,
    ELASTIC_SETTINGS,
    GENRES_STATE_PATH,
    MOVIES_STATE_PATH,
    PERSONS_STATE_PATH,
)
from core.logger import LOGGING
from custom_decorators import period
from extract import PostgresExtractor
from load import ElasticLoader
from sql import extract_queries
from state import JsonFileStorage, State
from transform import DataTransformer
from core.config import Settings

# Применяем настройки логирования
logging.config.dictConfig(LOGGING)

settings = Settings()


@period(10)
def etl(
    extractor: PostgresExtractor, transformer: DataTransformer, loader: ElasticLoader
) -> None:
    """Функция для последовательного запуска экземпляров ETL-процесса"""
    logging.warning("ETL process was started.")
    data = extractor.extract()
    transformed_data = transformer.transform(data)
    loader.load(transformed_data)


if __name__ == "__main__":

    states = {
        "movie": State(storage=JsonFileStorage(file_path=MOVIES_STATE_PATH)),
        "genre": State(storage=JsonFileStorage(file_path=GENRES_STATE_PATH)),
        "person": State(storage=JsonFileStorage(file_path=PERSONS_STATE_PATH)),
        "all_genres": State(storage=JsonFileStorage(file_path=ALL_GENRES_STATE_PATH)),
        "all_persons": State(storage=JsonFileStorage(file_path=ALL_PERSONS_STATE_PATH)),
    }

    movies_extractor = PostgresExtractor(
        dsn=settings.POSTGRES_DSN, query=extract_queries, state=states
    )
    movies_transformer = DataTransformer()
    movies_loader = ElasticLoader(
        conn=ELASTIC_PATH,
        index=ELASTIC_INDEX,
        settings=ELASTIC_SETTINGS,
        mappings=ALL_MAPPINGS,
        state=states,
    )
    while True:
        etl(
            extractor=movies_extractor,
            transformer=movies_transformer,
            loader=movies_loader,
        )
