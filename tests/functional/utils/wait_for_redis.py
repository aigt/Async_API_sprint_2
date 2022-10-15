import logging
import time

import aioredis

from settings import get_settings

if __name__ == '__main__':
    r_client = aioredis.from_url(
        get_settings().redis_dsn,
        encoding="utf-8",
        decode_responses=True,
    )
    while True:
        try:
            if r_client.ping():
                logging.info('Redis is connected.')
                break
        except (aioredis.ConnectionError, aioredis.TimeoutError):
            logging.info('Redis is not connected, retry in 1 seconds...')
            time.sleep(1)
        