import logging
from typing import Any, Callable

from elastic_transport import ConnectionError


def es_reconnect(extractor: Callable) -> Callable:
    """Декоратор для поаторного соединения с ElasticSearch"""

    def wrapper(process: Any, *args, **kwargs):
        if not process.connected():
            process.connect()
            logging.warning("Elastic connection is UP")

        try:
            return extractor(process, *args, **kwargs)
        except ConnectionError as err:
            logging.error("ES connection is DOWN: %s", err)
            process.close()
            raise

    return wrapper
