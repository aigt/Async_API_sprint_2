import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_persons


@pytest.mark.parametrize("query_data, expected",
                         [({'query': 'Mark', 'page[size]': 50}, {'status': 200, 'length': 2}),
                          ({'query': 'Unknown Person', 'page[size]': 50}, {'status': 404, 'length': 1}),
                          (None, {'status': 422, 'length': 1}),
                          ({'query': 'Mark', 'page[size]': 1}, {'status': 200, 'length': 1})])
@pytest.mark.asyncio
async def test_persons_search(es_write_data, make_get_request, query_data, expected):
    bulk_query = get_es_bulk_query(data=es_persons,
                                   index=test_settings.es_index['persons_search'],
                                   id_field='full_name')

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['persons_search'])

    url = test_settings.service_url + '/api/v1/persons/search'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert len(body) == expected['length']


@pytest.mark.parametrize("query_data, expected",
                         [({'query': 'mark', 'page[size]': 1, 'page[number]': 2}, {'status': 200, 'full_name': 'Mark Zuckerberg'})])
@pytest.mark.asyncio
async def test_persons_search_title(es_write_data, make_get_request, query_data, expected):
    bulk_query = get_es_bulk_query(data=es_persons,
                                   index=test_settings.es_index['persons_search'],
                                   id_field='full_name')

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['persons_search'])

    url = test_settings.service_url + '/api/v1/persons/search'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert body[0]['full_name'] == expected['full_name']