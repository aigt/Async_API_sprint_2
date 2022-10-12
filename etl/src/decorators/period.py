import time
from typing import Callable


def period(secs: int) -> Callable:
    """Декоратор для установки периодичности запуска etl-процесса"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> None:
            time.sleep(secs)
            return func(*args, **kwargs)

        return wrapper

    return decorator
