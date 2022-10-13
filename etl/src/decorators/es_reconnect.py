import logging
import time

from typing import Any, Callable
from functools import wraps
from elastic_transport import ConnectionError


def es_reconnect(extractor: Callable, start_sleep_time=0.1, factor=2, border_sleep_time=10) -> Callable:
    """Декоратор для повторного соединения с ElasticSearch"""
    @wraps(extractor)
    def wrapper(process: Any, *args, **kwargs):
        n = 0
        while True:
            if not process.connected():
                process.reconnect()
                logging.warning("Elastic connection is UP")
            try:
                return extractor(process, *args, **kwargs)
            except ConnectionError as err:
                sleep_time = start_sleep_time * (factor**n)
                if sleep_time > border_sleep_time:
                    sleep_time = border_sleep_time
                logging.info(f'Elastic connection failed {n+1}, try to reconnect. Exception: {err}')
                time.sleep(sleep_time)
                n += 1
    return wrapper
