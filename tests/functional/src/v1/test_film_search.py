import pytest

from testdata.load_to_es_data import es_films_search


@pytest.mark.parametrize(
    "query_data, expected",
    [
        ({'query': 'The Star', 'page[size]': 50}, {'status': 200, 'length': 50}),
        ({'query': 'Unknown Movie', 'page[size]': 50}, {'status': 404, 'length': 1}),
        (None, {'status': 422, 'length': 1}),
        ({'query': 'The Star', 'page[size]': 1}, {'status': 200, 'length': 1}),
    ],
)
@pytest.mark.asyncio
async def test_films_search(
    settings,
    es_write_data,
    make_get_request,
    query_data,
    expected,
):
    await es_write_data(index=settings.es_index['films_search'], id_field=settings.es_id_field, data=es_films_search)
    url = settings.service_url + '/api/v1/films/search'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert len(body) == expected['length']


@pytest.mark.parametrize(
    "query_data, expected",
    [
        ({'query': 'The Star', 'page[size]': 1, 'page[number]': 2}, {'status': 200, 'title': 'The Star 1'}),
    ],
)
@pytest.mark.asyncio
async def test_films_search_title(
    settings,
    es_write_data,
    make_get_request,
    query_data,
    expected,
):
    await es_write_data(index=settings.es_index['films_search'], id_field=settings.es_id_field, data=es_films_search)
    url = settings.service_url + '/api/v1/films/search'
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    assert status == expected['status']
    assert body[0]['title'] == expected['title']
