import logging
import os

logger = logging.getLogger("logger")

logging.basicConfig(
    filename="etl.log", format="%(levelname)s:%(message)s", level=logging.WARNING
)


# PG_DB_PATH = {
#     "dbname": os.getenv("POSTGRES_NAME"),
#     "user": os.getenv("POSTGRES_USER"),
#     "password": os.getenv("POSTGRES_PASSWORD"),
#     "host": os.getenv("POSTGRES_HOST"),
#     "port": os.getenv("POSTGRES_PORT"),
# }

PG_DB_PATH = {
    "dbname": "movies_db",
    "user": "app",
    "password": "123qwe",
    "host": "127.0.0.1",
    "port": 5432,
}


# ELASTIC_PATH = os.getenv("ELASTIC_PATH")
ELASTIC_PATH = "http://127.0.0.1:9200"


MOVIES_STATE_PATH = "save_movie_state.json"
GENRES_STATE_PATH = "save_genre_state.json"
PERSONS_STATE_PATH = "save_person_state.json"
ALL_GENRES_STATE_PATH = 'save_all_genres_state.json'


ELASTIC_SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {"type": "stemmer", "language": "english"},
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {"type": "stemmer", "language": "russian"},
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}


ELASTIC_MAPPINGS = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "imdb_rating": {"type": "float"},
        "genre": {"type": "keyword"},
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {"raw": {"type": "keyword"}},
        },
        "description": {"type": "text", "analyzer": "ru_en"},
        "director": {"type": "text", "analyzer": "ru_en"},
        "actors_names": {"type": "text", "analyzer": "ru_en"},
        "writers_names": {"type": "text", "analyzer": "ru_en"},
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

ELASTIC_MAPPINGS_ALL_GENRES = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "name": {"type": "text"},
    }
}

ALL_MAPPINGS = {
    "movies": ELASTIC_MAPPINGS,
    "genres": ELASTIC_MAPPINGS_ALL_GENRES
}


ELASTIC_INDEX = "movies"

ELASTIC_INDEX = {"movies": "movies",
                 "genres": "genres"}