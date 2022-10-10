import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_persons


@pytest.mark.asyncio
async def test_persons_search(es_write_data, make_get_request):
    bulk_query = get_es_bulk_query(data=es_persons,
                                   index=test_settings.es_index['persons_search'],
                                   id_field='full_name')

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['persons_search'])

    url = test_settings.service_url + '/api/v1/persons/search'
    # проверка успешного поиска с параметром query
    query_data = {'query': 'Mark', 'page[size]': 50}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 2

    # проверка поиска неизвестной персоны
    query_data = {'query': 'Unknown Person', 'page[size]': 50}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 404
    assert len(body) == 1

    # проверка ошибки при пустом значении query
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 422
    assert len(body) == 1

    # проверка вывода количества записей на страницу
    query_data = {'query': 'Mark', 'page[size]': 1}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 1

    # проверка вывода второй страницы
    query_data = {'query': 'Mark', 'page[size]': 1, 'page[number]': 2}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body[0]['full_name'] == 'Mark Zuckerberg'