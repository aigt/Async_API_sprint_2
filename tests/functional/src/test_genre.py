import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_genres


@pytest.mark.asyncio
async def test_genres(es_write_data, make_get_request):
    bulk_query = get_es_bulk_query(data=es_genres,
                                   index=test_settings.es_index['genres'],
                                   id_field="id")

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['genres'])
    url = test_settings.service_url + '/api/v1/genres/'

    # проверка успешного вывода всех жанров
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 4

    # проверка ограниничения количества жанров на страницу
    query_data = {'page[size]': 1}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 1

    # проверка вывода жанров на второй странице
    query_data = {'page[size]': 1, 'page[number]': 2}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body[0]['name'] == 'Drama'

    # проверка поиска жанра по id
    url_id = url + es_genres[0]['id']
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body['name'] == 'Sci-Fi'

    # проверка поиска жанра по неизвестному id
    url_id = url + 'fa189edd-9f2b-4d21-ac33-895890a93632'
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 404
    assert body['detail'] == 'genre not found'

    # проверка поиска жанра по нневалидному id
    url_id = url + 'some invalid id'
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 422


