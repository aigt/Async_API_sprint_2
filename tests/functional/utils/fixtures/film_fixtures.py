import pytest

from testdata.load_to_es_data import es_films, es_films_search


@pytest.fixture(scope="module")
def prepare_film_search_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['films_search'],
            id_field=settings.es_id_field,
            data=es_films_search,
        )
    )


@pytest.fixture(scope="module")
def prepare_film_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['films'],
            id_field='id',
            data=es_films,
        )
    )