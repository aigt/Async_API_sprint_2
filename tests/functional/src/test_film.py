import pytest
import sys
sys.path.append('../..')

from tests.functional.settings import test_settings
from tests.functional.testdata.conftest import get_es_bulk_query, es_client, es_write_data, make_get_request, aiohttp_session
from tests.functional.testdata.load_to_es_data import es_films_search, es_films


@pytest.mark.asyncio
async def test_films(es_write_data, make_get_request):
    bulk_query = get_es_bulk_query(data=es_films,
                                   index=test_settings.es_index['films'],
                                   id_field='id')

    await es_write_data(bulk_query=bulk_query, index=test_settings.es_index['films'])
    url = test_settings.service_url + '/api/v1/films/'

    # проверка успешного вывода всех фильмов
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 2

    # проверка ограниничения количества фильмов на страницу
    query_data = {'page[size]': 1}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert len(body) == 1

    # проверка вывода фильмов на второй странице
    query_data = {'page[size]': 1, 'page[number]': 2}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body[0]['title'] == 'The Shining'

    # проверка работы сортировки по рейтингу (убывание)
    query_data = {'sort': '-imdb_rating'}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body[0]['title'] == 'The Shining'

    # проверка работы фильтрации по жанру
    query_data = {'filter[genre]': 'horror'}
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body[0]['title'] == 'The Shining'

    # проверка поиска фильма по id
    url_id = url + es_films[0]['id']
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 200
    assert body['title'] == 'Star Wars'

    # проверка поиска фильма по неизвестному id
    url_id = url + 'fa189edd-9f2b-4d21-ac33-895890a93632'
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 404
    assert body['detail'] == 'film not found'

    # проверка поиска фильма по невалидному id
    url_id = url + 'some invalid id'
    response = await make_get_request(url=url_id, query_data=None)
    body = await response.json()
    status = response.status
    assert status == 422

