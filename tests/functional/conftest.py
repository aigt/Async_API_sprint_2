import asyncio
import json

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from settings import get_settings


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def settings():
    return get_settings()


def get_es_bulk_query(data, index, id_field):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': row[id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


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


@pytest.fixture()
def es_write_data(es_client):
    async def inner(bulk_query: list[dict], index):
        str_query = '\n'.join(bulk_query) + '\n'
        index_exists = await es_client.indices.exists(index=index)
        index_delete = await es_client.options(ignore_status=[400, 404]).indices.delete(index=index)
        if index_exists:
            index_delete
        response = await es_client.bulk(operations=str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture()
def make_get_request(aiohttp_session):
    async def inner(url, query_data):
        response = await aiohttp_session.get(url, params=query_data)
        return response
    return inner