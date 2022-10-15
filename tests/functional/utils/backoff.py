import logging
import time
from functools import wraps
from typing import Any, Callable


class BackoffMaxTriesException(Exception):
    """Исключение вызываемое после достижения максимального количества попыток."""

    def __init__(self, max_tries: int, func: Callable[..., Any]):
        self.max_tries = max_tries
        self.func = func
        self.message = f'number of tries ({max_tries}) to call function {func.__name__} exceeded.'
        super().__init__(self.message)


def backoff(
    exceptions: tuple[Exception] | Exception = Exception,
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
    max_tries: int = 15,
) -> Callable[..., Any]:
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка. Использует наивный экспоненциальный рост времени
    повтора (factor) до граничного времени ожидания (border_sleep_time)
    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора, секунд
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания, секунд
    :param max_tries: максимальное количество попыток
    :return: результат выполнения функции
    """

    def func_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def retry(*args, **kwargs) -> Any:
            try_number = 0
            while True:
                try:
                    logging.info(f'try to execute {func.__name__}')
                    res = func(*args, **kwargs)
                    return res
                except exceptions as e:
                    logging.exception(f'filed {try_number+1} try to execute {func.__name__}')
                    sleep_time = start_sleep_time * (factor**try_number)
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time

                    logging.exception(
                        f'failed {try_number+1} try to execute {func.__name__} with exception: \n{e}\nnow sleep for {sleep_time}s'
                    )
                    time.sleep(sleep_time)
                    try_number += 1
                    
                    if 0 < max_tries <= try_number:
                        raise BackoffMaxTriesException(max_tries, func)
                

        return retry

    return func_wrapper
