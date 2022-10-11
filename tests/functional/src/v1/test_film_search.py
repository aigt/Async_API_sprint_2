import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_films_search, es_films


@pytest.mark.parametrize("query_data, expected",
                         [({'query': 'The Star', 'page[size]': 50}, {'status': 200, 'length': 50}),
                          ({'query': 'Unknown Movie', 'page[size]': 50}, {'status': 404, 'length': 1}),
                          (None, {'status': 422, 'length': 1}),
                          ({'query': 'The Star', 'page[size]': 1}, {'status': 200, 'length': 1})])
@pytest.mark.asyncio
async def test_films_search(es_write_data, make_get_request, query_data, expected):
    bulk_query = get_es_bulk_query(data=es_films_search,
                                   index=test_settings.es_index['films_search'],
                                   id_field=test_settings.es_id_field)

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['films_search'])

    url = test_settings.service_url + '/api/v1/films/search'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert len(body) == expected['length']


@pytest.mark.parametrize("query_data, expected",
                         [({'query': 'The Star', 'page[size]': 1, 'page[number]': 2}, {'status': 200, 'title': 'The Star 1'})])

@pytest.mark.asyncio
async def test_films_search_title(es_write_data, make_get_request, query_data, expected):
    bulk_query = get_es_bulk_query(data=es_films_search,
                                   index=test_settings.es_index['films_search'],
                                   id_field=test_settings.es_id_field)

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['films_search'])

    url = test_settings.service_url + '/api/v1/films/search'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert body[0]['title'] == expected['title']
