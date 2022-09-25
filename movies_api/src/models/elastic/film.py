from models.elastic.base import film_work


class Film(film_work.FilmWork):
    """Фильм"""

    imdb_rating: float
