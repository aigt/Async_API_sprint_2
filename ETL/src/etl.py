import logging.config

from core.config import get_settings
from core.logger import LOGGING
from custom_decorators import period
from extract import PostgresExtractor
from load import ElasticLoader
from schemas import elastic as es_schemas
from sql import extract_queries
from state import JsonFileStorage, State
from transform import DataTransformer

# Применяем настройки логирования
logging.config.dictConfig(LOGGING)

settings = get_settings()


@period(60 * 10)
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
        "movie": State(storage=JsonFileStorage(file_path=settings.MOVIES_STATE_PATH)),
        "genre": State(storage=JsonFileStorage(file_path=settings.GENRES_STATE_PATH)),
        "person": State(storage=JsonFileStorage(file_path=settings.PERSONS_STATE_PATH)),
        "all_genres": State(
            storage=JsonFileStorage(file_path=settings.ALL_GENRES_STATE_PATH)
        ),
        "all_persons": State(
            storage=JsonFileStorage(file_path=settings.ALL_PERSONS_STATE_PATH)
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
