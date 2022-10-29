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
        "subscription": {"type": "boolean"},
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
        "name": {"type": "text", "analyzer": "ru_en"},
    },
}

ELASTIC_MAPPINGS_ALL_PERSONS = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "full_name": {"type": "text", "analyzer": "ru_en"},
        "roles": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "role": {"type": "text", "analyzer": "ru_en"},
                "film_id": {"type": "keyword"},
                "film_title": {"type": "text", "analyzer": "ru_en"},
                "film_imdb_rating": {"type": "float"},
            },
        },
    },
}

ALL_MAPPINGS = {
    "movies": ELASTIC_MAPPINGS,
    "genres": ELASTIC_MAPPINGS_ALL_GENRES,
    "persons_v2": ELASTIC_MAPPINGS_ALL_PERSONS,
}


ELASTIC_INDEX = {"movies": "movies", "genres": "genres", "persons_v2": "persons_v2"}
