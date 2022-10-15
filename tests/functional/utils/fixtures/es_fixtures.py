import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from utils.es_bulk_query import get_es_bulk_query


@pytest_asyncio.fixture(scope="session")
async def es_client(settings):
    client = AsyncElasticsearch(hosts=settings.es_host,
                                verify_certs=False)
    yield client
    await client.close()


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