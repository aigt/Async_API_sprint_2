import pytest

from testdata.load_to_es_data import es_persons


@pytest.fixture(scope="module")
def prepare_person_search_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['persons_search'],
            id_field='full_name',
            data=es_persons,
        )
    )


@pytest.fixture(scope="module")
def prepare_person_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['persons'],
            id_field='id',
            data=es_persons,
        )
    )
