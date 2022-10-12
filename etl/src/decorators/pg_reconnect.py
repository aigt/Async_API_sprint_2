import logging
import time
from typing import Any, Callable
from functools import wraps

import psycopg2


def pg_reconnect(extractor: Callable, start_sleep_time=0.1, factor=2, border_sleep_time=10) -> Callable:
    """Декоратор для повторного соединения с Postgres"""
    @wraps(extractor)
    def wrapper(process: Any, *args, **kwargs) -> Callable:
        n = 0
        while True:
            if not process.connected():
                process.connect()
                logging.warning("PG connection is UP")
            try:
                return extractor(process, *args, **kwargs)
            except psycopg2.Error as err:
                sleep_time = start_sleep_time * (factor**n)
                if sleep_time > border_sleep_time:
                    sleep_time = border_sleep_time
                logging.info(f'postgres connection failed {n+1}, try to reconnect. Exception: {err}')
                time.sleep(sleep_time)
                n += 1
    return wrapper
