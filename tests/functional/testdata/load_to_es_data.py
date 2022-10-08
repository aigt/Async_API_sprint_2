import uuid
import datetime

es_films_search = [{
    'id': str(uuid.uuid4()),
    'imdb_rating': 8.5,
    'genre': ['Action', 'Sci-Fi'],
    'title': 'The Star' + ' ' + str(number),
    'description': 'New World',
    'director': 'Stan',
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': str(uuid.uuid4()), 'name': 'Ann'},
        {'id': str(uuid.uuid4()), 'name': 'Bob'}
    ],
    'writers': [
        {'id': str(uuid.uuid4()), 'name': 'Ben'},
        {'id': str(uuid.uuid4()), 'name': 'Howard'}
    ],
    'created_at': datetime.datetime.now().isoformat(),
    'updated_at': datetime.datetime.now().isoformat(),
    'film_work_type': 'movie'
} for number in range(60)]

es_films = [{
    'id': str(uuid.uuid4()),
    'imdb_rating': 7,
    'genre': ['Action'],
    'title': 'Star Wars',
    'description': 'New World',
    'director': 'Stan',
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': str(uuid.uuid4()), 'name': 'Ann'},
        {'id': str(uuid.uuid4()), 'name': 'Bob'}
    ],
    'writers': [
        {'id': str(uuid.uuid4()), 'name': 'Ben'},
        {'id': str(uuid.uuid4()), 'name': 'Howard'}
    ],
    'created_at': datetime.datetime.now().isoformat(),
    'updated_at': datetime.datetime.now().isoformat(),
    'film_work_type': 'movie'
},
{
    'id': str(uuid.uuid4()),
    'imdb_rating': 9,
    'genre': ['Horror'],
    'title': 'The Shining',
    'description': 'New World',
    'director': 'Stan',
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': str(uuid.uuid4()), 'name': 'Ann'},
        {'id': str(uuid.uuid4()), 'name': 'Bob'}
    ],
    'writers': [
        {'id': str(uuid.uuid4()), 'name': 'Ben'},
        {'id': str(uuid.uuid4()), 'name': 'Howard'}
    ],
    'created_at': datetime.datetime.now().isoformat(),
    'updated_at': datetime.datetime.now().isoformat(),
    'film_work_type': 'movie'
}]