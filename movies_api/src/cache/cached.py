import logging
from functools import wraps

from core.config import get_settings
from db.redis import get_redis

settings = get_settings()


def cached_id_item(*, id_name: str):
    """Декоратор кэширует функцию в редисе по значению параметра id_name.

    Args:
        id_name (str): Имя параметра в функции, который будет служить ключём
    """

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            redis = await get_redis()

            key = f'{func.__name__}:{id_name}:{kwargs[id_name]}'

            data = await redis.get(key)
            if not data:
                logging.info(f'no data in cache with key: {key}')

                data = (await func(*args, **kwargs)).json()
                if data is None:
                    logging.info(f'no data in func: {func.__name__}')
                    return None

                await redis.set(
                    key,
                    data,
                    ex=settings.CACHE_EXPIRE_IN_SECONDS,
                )

            logging.info(f'data with key {key}: {data}')
            v_type = func.__annotations__['return']
            return v_type.parse_raw(data)

        return inner

    return func_wrapper
