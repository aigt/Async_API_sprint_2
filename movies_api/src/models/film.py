from models.base import film_work


class Film(film_work.FilmWork):
    """Фильм"""

    imdb_rating: float
