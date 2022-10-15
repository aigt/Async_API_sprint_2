import logging

import aioredis

from settings import get_settings
from utils.backoff import backoff


class RedisIsNotConnected(Exception):
    """Исключение вызываемое если не удалось подключиться к Redis."""
    pass


@backoff()
def wait_for_redis():
    r_client = aioredis.from_url(
        get_settings().redis_dsn,
        encoding="utf-8",
        decode_responses=True,
    )
    
    if r_client.ping():
        logging.info('Redis is connected.')
        return
    
    raise RedisIsNotConnected('Redis is not connected.')
    


if __name__ == '__main__':
    wait_for_redis()
        