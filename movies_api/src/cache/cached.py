import logging
from functools import wraps

import backoff
from aioredis import RedisError

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
            @backoff.on_exception(backoff.expo, RedisError, max_time=20)
            async def set_cache(key: str, data: str) -> None:
                await redis.set(key, data, ex=settings.CACHE_EXPIRE_IN_SECONDS)
            
            @backoff.on_exception(backoff.expo, RedisError, max_time=20)
            async def get_cache(key: str) -> str:
                return await redis.get(key)
            
            redis = await get_redis()

            key = f'{func.__name__}:{id_name}:{kwargs[id_name]}'

            data = await get_cache(key)
            if not data:
                logging.debug(f'no data in cache with key: {key}')

                data = await func(*args, **kwargs)
                
                if data is None:
                    logging.debug(f'no data in func: {func.__name__}')
                    return None

                logging.debug(f'save in cache: {key}::{data}')
                await set_cache(key, data.json())
                return data

            logging.debug(f'data with key {key}: {data}')
            return_type = func.__annotations__['return'].__args__[0]
            return return_type.parse_raw(data)

        return inner

    return func_wrapper
