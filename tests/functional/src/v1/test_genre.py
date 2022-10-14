import pytest

from testdata.load_to_es_data import es_genres


@pytest.mark.parametrize(
    "query_data, expected",
    [
        (None, {"status": 200, "length": 4}),
        ({'page[size]': 1}, {"status": 200, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_genres(
    settings,
    es_write_data,
    make_get_request,
    query_data,
    expected,
):
    await es_write_data(index=settings.es_index['genres'], id_field='id', data=es_genres)
    url = settings.service_url + '/api/v1/genres/'
    # проверка успешного вывода всех фильмов
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert len(body) == expected['length']


@pytest.mark.parametrize(
    "query_data, expected",
    [
        ({'page[size]': 1, 'page[number]': 2}, {"status": 200, "name": 'Drama'}),
    ],
)
@pytest.mark.asyncio
async def test_genres_name(
    settings,
    es_write_data,
    make_get_request,
    query_data,
    expected
):
    await es_write_data(index=settings.es_index['genres'], id_field='id', data=es_genres)
    url = settings.service_url + '/api/v1/genres/'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert  body[0]['name'] == expected['name']


@pytest.mark.parametrize(
    "genre_id, expected",
    [
        (es_genres[0]['id'], {'status': 200, 'name': 'Sci-Fi'}),
    ],
)
@pytest.mark.asyncio
async def test_genres_id(
    settings,
    es_write_data,
    make_get_request,
    genre_id,
    expected,
):
    await es_write_data(index=settings.es_index['genres'], id_field='id', data=es_genres)
    url = settings.service_url + '/api/v1/genres/' + genre_id
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert body['name'] == expected['name']


@pytest.mark.parametrize(
    "genre_id, expected",
    [
        ('fa189edd-9f2b-4d21-ac33-895890a93632', {'status': 404}),
        ('some invalid id', {'status': 422}),
    ],
)
@pytest.mark.asyncio
async def test_films_invalid_id(
    settings,
    es_write_data,
    make_get_request,
    genre_id,
    expected
):
    await es_write_data(index=settings.es_index['genres'], id_field='id', data=es_genres)
    url = settings.service_url + '/api/v1/genres/' + genre_id
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    assert status == expected['status']
