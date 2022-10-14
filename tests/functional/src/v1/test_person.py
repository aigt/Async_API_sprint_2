import pytest

from testdata.load_to_es_data import es_persons


@pytest.mark.parametrize(
    "query_data, expected",
    [
        (None, {"status": 200, "length": 4}),
        ({'page[size]': 1}, {"status": 200, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_persons(
    settings,
    es_write_data,
    make_get_request,
    query_data,
    expected
):
    # Arrange
    await es_write_data(index=settings.es_index['persons'], id_field='id', data=es_persons)
    url = settings.service_url + '/api/v1/persons/'
    
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
        ({'page[size]': 1, 'page[number]': 2}, {"status": 200, "full_name": 'Mark Hamill'}),
    ],
)
@pytest.mark.asyncio
async def test_persons_full_name(
    settings,
    es_write_data,
    make_get_request,
    query_data,
    expected,
):
    # Arrange
    await es_write_data(index=settings.es_index['persons'], id_field='id', data=es_persons)
    url = settings.service_url + '/api/v1/persons/'
    
    # Act
    response = await make_get_request(url=url, query_data=query_data)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert  body[0]['full_name'] == expected['full_name']


@pytest.mark.parametrize(
    "person_id, expected",
    [
        (
            es_persons[1]['id'],
            {
                'status': 200,
                'full_name': 'Mark Hamill',
                'film_ids': len(es_persons[1]['roles']),
                'role': ['actor'],
            }
        ),
    ],
)
@pytest.mark.asyncio
async def test_persons_id(
    settings,
    es_write_data,
    make_get_request,
    person_id,
    expected,
):
    # Arrange
    await es_write_data(index=settings.es_index['persons'], id_field='id', data=es_persons)
    url = settings.service_url + '/api/v1/persons/' + person_id
    
    # Act
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert body['full_name'] == expected['full_name']
    assert len(body['film_ids']) == expected['film_ids']
    assert body['role'] == expected['role']


@pytest.mark.parametrize(
    "person_id, expected",
    [
        ('fa189edd-9f2b-4d21-ac33-895890a93632', {'status': 404}),
        ('some invalid id', {'status': 422}),
    ],
)
@pytest.mark.asyncio
async def test_persons_invalid_id(
    settings,
    es_write_data,
    make_get_request,
    person_id,
    expected,
):
    # Arrange
    await es_write_data(index=settings.es_index['persons'], id_field='id', data=es_persons)
    url = settings.service_url + '/api/v1/persons/' + person_id
    
    # Act
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']


@pytest.mark.parametrize(
    "person_id, expected",
    [
        (es_persons[1]['id'], {"status": 200, "movie_count": 36}),
    ],
)
@pytest.mark.asyncio
async def test_persons_films(
    settings,
    es_write_data,
    make_get_request,
    person_id,
    expected
):
    # Arrange
    await es_write_data(index=settings.es_index['persons'], id_field='id', data=es_persons)
    url = settings.service_url + '/api/v1/persons/' + person_id + '/film'
    
    # Act
    response = await make_get_request(url=url, query_data=None)
    body = await response.json()
    status = response.status
    
    # Assert
    assert status == expected['status']
    assert len(body[0]['uuid']) == expected['movie_count']
