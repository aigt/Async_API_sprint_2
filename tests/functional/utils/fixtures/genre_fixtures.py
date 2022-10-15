
import pytest

from testdata.load_to_es_data import es_genres


@pytest.fixture(scope="module")
def prepare_genre_es_data(settings, es_write_data, event_loop):
    event_loop.run_until_complete(
        es_write_data(
            index=settings.es_index['genres'],
            id_field='id',
            data=es_genres,
        )
    )
