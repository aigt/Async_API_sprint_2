import pytest

from testdata.load_to_es_data import es_films


@pytest.mark.parametrize(
    "query_data, expected",
    [
        (None, {"status": 200, "length": 2}),
        ({'page[size]': 1}, {"status": 200, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_films(
    settings,
    prepare_film_es_data,
    make_get_request,
    query_data,
    expected,
):
    # Arrange
    url = settings.service_url + '/api/v1/films/'
    
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
        ({'page[size]': 1, 'page[number]': 2}, {"status": 200, "title": 'The Shining'}),
        ({'sort': '-imdb_rating'}, {"status": 200, "title": 'The Shining'}),
        ({'filter[genre]': 'horror'}, {"status": 200, "title": 'The Shining'}),
    ],
)
@pytest.mark.asyncio
async def test_films_title(
    settings,
    prepare_film_es_data,
    make_get_request,
    query_data,
    expected,
):
    # Arrange
    url = settings.service_url + '/api/v1/films/'
    
    # Act
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert body[0]['title'] == expected['title']


@pytest.mark.parametrize(
    "film_id, expected",
    [
        (es_films[0]['id'], {'status': 200, 'title': 'Star Wars'}),
    ],
)
@pytest.mark.asyncio
async def test_films_id(
    settings,
    prepare_film_es_data,
    make_get_request,
    film_id,
    expected,
):
    # Arrange
    url = settings.service_url + '/api/v1/films/' + film_id
    
    # Act
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert body['title'] == expected['title']


@pytest.mark.parametrize(
    "film_id, expected",
    [
        ('fa189edd-9f2b-4d21-ac33-895890a93632', {'status': 404}),
        ('some invalid id', {'status': 422}),
    ],
)
@pytest.mark.asyncio
async def test_films_invalid_id(
    settings,
    prepare_film_es_data,
    make_get_request,
    film_id,
    expected,
):
    # Arrange
    url = settings.service_url + '/api/v1/films/' + film_id
    
    # Act
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
