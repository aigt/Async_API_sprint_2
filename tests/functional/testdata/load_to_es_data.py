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

es_genres = [{
    'id': "39220b3b-f9bc-4ca2-a02f-810a014d9919",
    'name': 'Sci-Fi'
},
{
    'id': "25ba6836-ac3c-4bf2-bb19-d003c1585c7a",
    'name': 'Drama'
},
{
    'id': "fa189edd-9f2b-4d21-ac33-895890a93631",
    'name': 'Horror'
},
{
    'id': "d3199589-f34a-4845-88c7-d36bcef14b5a",
    'name': 'Comedy'
}]


es_persons = [
    {
    "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
    "full_name": "Jeorge Lucas",
    "roles": [{
                "role": "actor",
                "film_id": "19babc93-62f5-481a-b6fe-9ebfef689cbc",
                "film_title": "Star Wars: The Legacy Revealed",
                "film_imdb_rating": 7.8
                },
                {
                "role": "director",
                "film_id": "d4b010a5-2648-4850-b15d-307658020923",
                "film_title": "Lego Star Wars: Revenge of the Brick",
                "film_imdb_rating": 6.1
                },]
    },
    {
        "id": "26e83050-29ef-4163-a99d-b546cac208f8",
        "full_name": "Mark Hamill",
        "roles": [{
            "role": "actor",
            "film_id": "943946ed-4a2b-4c71-8e0b-a58a11bd1323",
            "film_title": "Star Wars: Evolution of the Lightsaber Duel",
            "film_imdb_rating": 6.8
        },
            {
                "role": "actor",
                "film_id": "3a28f10a-433e-431c-8e7b-cc3f90af5a41",
                "film_title": "The Making of 'Star Wars'",
                "film_imdb_rating": 7.5
            }, ]
    },
    {
        "id": "a1758395-9578-41af-88b8-3f9456e6d938",
        "full_name": "J.J. Abrams",
        "roles": [{
            "role": "actor",
            "film_id": "075587eb-91c1-4629-adcb-67c516cdb6eb",
            "film_title": "Star Trek: A New Vision",
            "film_imdb_rating": 6.8
        },
            {
            "role": "director",
            "film_id": "4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f",
            "film_title": "Star Trek",
            "film_imdb_rating": 7.9
            }, ]
    },
    {
        "id": "efdd1787-8871-4aa9-b1d7-f68e55b913ed",
        "full_name": "Billy Dee Williams",
        "roles": [{
            "role": "actor",
            "film_id": "025c58cd-1b7e-43be-9ffb-8571a613579b",
            "film_title": "Star Wars: Episode VI - Return of the Jedi",
            "film_imdb_rating": 8.3
        }]
    },
]


