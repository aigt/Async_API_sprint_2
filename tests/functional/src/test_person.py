import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_persons


@pytest.mark.asyncio
async def test_persons(es_write_data, make_get_request):
    bulk_query = get_es_bulk_query(data=es_persons,
                                   index=test_settings.es_index['persons'],
                                   id_field="id")

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['persons'])
    url = test_settings.service_url + '/api/v1/persons/'

    # проверка успешного вывода всех персон
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 4

    # проверка ограниничения количества персон на страницу
    query_data = {'page[size]': 1}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 1

    # проверка вывода персон на второй странице
    query_data = {'page[size]': 1, 'page[number]': 2}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body[0]['full_name'] == 'Mark Hamill'

    # проверка поиска персоны по id
    url_id = url + es_persons[0]['id']
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body['full_name'] == 'Jeorge Lucas'

    # проверка вывода id фильмов для персоны
    url_id = url + es_persons[0]['id']
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body['film_ids'] == [i['film_id'] for i in es_persons[0]['roles']]

    # проверка вывода ролей персоны
    url_id = url + es_persons[1]['id']
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body['role'] == ['actor']

    # проверка поиска персоны по неизвестному id
    url_id = url + 'fa189edd-9f2b-4d21-ac33-895890a93632'
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 404
    assert body['detail'] == 'person not found'

    # проверка поиска персоны по нневалидному id
    url_id = url + 'some invalid id'
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 422

