import asyncio

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from settings import get_settings
from testdata.load_to_es_data import (es_films, es_films_search, es_genres,
                                      es_persons)
from utils.es_bulk_query import get_es_bulk_query


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest_asyncio.fixture(scope="session")
async def es_client(settings):
    client = AsyncElasticsearch(hosts=settings.es_host,
                                verify_certs=False)
    yield client
    await client.close()


@pytest_asyncio.fixture()
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def es_write_data(es_client):
    async def inner(index, id_field, data):
        bulk_query = get_es_bulk_query(data=data, index=index, id_field=id_field)
        str_query = '\n'.join(bulk_query) + '\n'
        index_exists = await es_client.indices.exists(index=index)
        index_delete = await es_client.options(ignore_status=[400, 404]).indices.delete(index=index)
        if index_exists:
            index_delete
        response = await es_client.bulk(operations=str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture(scope="module")
def prepare_film_search_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['films_search'],
            id_field=settings.es_id_field,
            data=es_films_search,
        )
    )


@pytest.fixture(scope="module")
def prepare_film_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['films'],
            id_field='id',
            data=es_films,
        )
    )


@pytest.fixture(scope="module")
def prepare_genre_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['genres'],
            id_field='id',
            data=es_genres,
        )
    )


@pytest.fixture(scope="module")
def prepare_person_search_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['persons_search'],
            id_field='full_name',
            data=es_persons,
        )
    )


@pytest.fixture(scope="module")
def prepare_person_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['persons'],
            id_field='id',
            data=es_persons,
        )
    )


@pytest.fixture()
def make_get_request(aiohttp_session):
    async def inner(url, query_data):
        response = await aiohttp_session.get(url, params=query_data)
        return response
    return inner