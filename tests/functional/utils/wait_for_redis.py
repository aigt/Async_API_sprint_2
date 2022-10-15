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
                print('Redis connected.')
                break
        except (aioredis.ConnectionError, aioredis.TimeoutError):
            print('Redis not connected, retry in 1 seconds...')
            time.sleep(1)
        