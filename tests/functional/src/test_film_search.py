import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_films_search, es_films


@pytest.mark.asyncio
async def test_films_search(es_write_data, make_get_request):
    bulk_query = get_es_bulk_query(data=es_films_search,
                                   index=test_settings.es_index['films_search'],
                                   id_field=test_settings.es_id_field)

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['films_search'])

    url = test_settings.service_url + '/api/v1/films/search'
    # проверка успешного поиска с параметром query
    query_data = {'query': 'The Star', 'page[size]': 50}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 50

    # проверка поиска неизвестного фильма
    query_data_unknown = {'query': 'Unknown Movie', 'page[size]': 50}
    response_unknown = await make_get_request(url=url, query_data=query_data_unknown)
    body_unknown = await response_unknown.json()
    status_unknown = response_unknown.status
    assert status_unknown == 404
    assert len(body_unknown) == 1

    # проверка ошибки при пустом значении query
    response_empty = await make_get_request(url=url, query_data=None)
    body_empty = await response_empty.json()
    status_empty = response_empty.status
    assert status_empty == 422
    assert len(body_empty) == 1
