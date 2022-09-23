import os

from config import (ELASTIC_INDEX, ELASTIC_MAPPINGS, ELASTIC_PATH,
                    ELASTIC_SETTINGS, GENRES_STATE_PATH, MOVIES_STATE_PATH,
                    PERSONS_STATE_PATH, PG_DB_PATH, logger)
from custom_decorators import period
from extract import PostgresExtractor
from load import ElasticLoader
from sql import extract_queries
from state import JsonFileStorage, State
from transform import DataTransformer


@period(10)
def etl(
    extractor: PostgresExtractor, transformer: DataTransformer, loader: ElasticLoader
) -> None:
    """Функция для последовательного запуска экземпляров ETL-процесса"""
    logger.warning("ETL process was started.")
    data = extractor.extract()
    transformed_data = transformer.transform(data)
    loader.load(transformed_data)


if __name__ == "__main__":

    states = {
        "movie": State(storage=JsonFileStorage(file_path=MOVIES_STATE_PATH)),
        "genre": State(storage=JsonFileStorage(file_path=GENRES_STATE_PATH)),
        "person": State(storage=JsonFileStorage(file_path=PERSONS_STATE_PATH)),
    }

    movies_extractor = PostgresExtractor(
        conn=PG_DB_PATH, query=extract_queries, state=states
    )
    movies_transformer = DataTransformer()
    movies_loader = ElasticLoader(
        conn=ELASTIC_PATH,
        index=ELASTIC_INDEX,
        settings=ELASTIC_SETTINGS,
        mappings=ELASTIC_MAPPINGS,
        state=states,
    )
    while True:
        etl(
            extractor=movies_extractor,
            transformer=movies_transformer,
            loader=movies_loader,
        )
