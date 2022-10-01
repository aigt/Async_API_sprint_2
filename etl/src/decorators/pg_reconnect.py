import logging
from typing import Any, Callable

import psycopg2


def pg_reconnect(extractor: Callable) -> Callable:
    """Декоратор для повторного соединения с Postgres"""

    def wrapper(process: Any, *args, **kwargs) -> Callable:
        if not process.connected():
            process.connect()
            logging.warning("PG connection is UP")

        try:
            return extractor(process, *args, **kwargs)
        except psycopg2.Error as err:
            logging.error("PG connection is DOWN: %s", err)
            process.close()
            raise

    return wrapper
