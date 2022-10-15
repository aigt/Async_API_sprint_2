import aioredis
import pytest_asyncio


@pytest_asyncio.fixture(scope='session')
async def redis_client(settings):
    redis = await aioredis.from_url(
        settings.redis_dsn,
        encoding="utf-8",
        decode_responses=True,
    )
    yield redis
    await redis.close()
    await redis.connection_pool.disconnect()