import aiohttp
import pytest
import pytest_asyncio


@pytest_asyncio.fixture()
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
def make_get_request(aiohttp_session):
    async def inner(url, query_data):
        response = await aiohttp_session.get(url, params=query_data)
        return response
    return inner