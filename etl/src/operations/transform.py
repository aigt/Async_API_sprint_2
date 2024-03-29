from models.genre import Genre
from models.movie import Movie
from models.person import Person


class DataTransformer:
    """Преобразование данных"""

    def transform(self, data) -> list:
        """Функция преобразует данные из DictRow в Dataclass"""
        validated_data = [Movie(*dict(i).values()) for i in data[0]]

        validated_data_all_genres = [Genre(*dict(i).values()) for i in data[1]]

        validated_data_all_persons = [Person(**person) for person in data[2]]

        return (validated_data, validated_data_all_genres, validated_data_all_persons)
