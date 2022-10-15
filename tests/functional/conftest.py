import asyncio
import pytest

from settings import get_settings


pytest_plugins = ("utils.fixtures.redis_fixtures",
                  "utils.fixtures.es_fixtures",
                  "utils.fixtures.aiohttp_fixtures",
                  "utils.fixtures.film_fixtures",
                  "utils.fixtures.genre_fixtures",
                  "utils.fixtures.person_fixtures"
                  )


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings():
    return get_settings()
