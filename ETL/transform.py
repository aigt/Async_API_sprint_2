from models import Movie


class DataTransformer:
    """Преобразование данных"""

    def transform(self, data) -> list:
        """Функция преобразует данные из DictRow в Dataclass"""
        validated_data = [Movie(*dict(i).values()) for i in data]
        return validated_data
