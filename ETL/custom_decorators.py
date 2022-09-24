import time
from typing import Any, Callable

import psycopg2
from config import logger
from elastic_transport import ConnectionError


def period(secs: int) -> Callable:
    """Декоратор для установки периодичности запуска etl-процесса"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            time.sleep(secs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def pg_reconnect(extractor: Callable) -> Callable:
    """Декоратор для повторного соединения с Postgres"""

    def wrapper(process: Any, *args, **kwargs) -> Callable:
        if not process.connected():
            process.connect()
            logger.warning("PG connection is UP")

        try:
            return extractor(process, *args, **kwargs)
        except psycopg2.Error as err:
            logger.error("PG connection is DOWN: %s", err)
            process.close()
            raise

    return wrapper


def es_reconnect(extractor: Callable) -> Callable:
    """Декоратор для поаторного соединения с ElasticSearch"""

    def wrapper(process: Any, *args, **kwargs):
        if not process.connected():
            process.connect()
            logger.warning("Elastic connection is UP")

        try:
            return extractor(process, *args, **kwargs)
        except ConnectionError as err:
            logger.error("ES connection is DOWN: %s", err)
            process.close()
            raise

    return wrapper
