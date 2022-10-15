from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, expected",
    [
        ({'query': 'The Star', 'page[size]': 50}, {'status': HTTPStatus.OK, 'length': 50}),
        ({'query': 'Unknown Movie', 'page[size]': 50}, {'status': HTTPStatus.NOT_FOUND, 'length': 1}),
        (None, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}),
        ({'query': 'The Star', 'page[size]': 1}, {'status': HTTPStatus.OK, 'length': 1}),
    ],
)
@pytest.mark.asyncio
async def test_films_search(
    settings,
    prepare_film_search_es_data,
    redis_client,
    make_get_request,
    query_data,
    expected,
):
    # Arrange
    await redis_client.flushall()
    url = settings.service_url + '/api/v1/films/search'
    
    # Act
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert len(body) == expected['length']


@pytest.mark.parametrize(
    "query_data, expected",
    [
        ({'query': 'The Star', 'page[size]': 1, 'page[number]': 2}, {'status': HTTPStatus.OK, 'title': 'The Star 1'}),
    ],
)
@pytest.mark.asyncio
async def test_films_search_title(
    settings,
    prepare_film_search_es_data,
    redis_client,
    make_get_request,
    query_data,
    expected,
):
    # Arrange
    await redis_client.flushall()
    url = settings.service_url + '/api/v1/films/search'
    
    # Act
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert body[0]['title'] == expected['title']
