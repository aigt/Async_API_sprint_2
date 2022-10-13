import abc
import json
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    """Хранение состояния на диске в формате json"""

    def __init__(self, file_path: str | None = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """Функция сохраняет состояние на диск в формате json"""
        with open(self.file_path, "w+") as json_data:
            json.dump(state, json_data, default=str)

    def retrieve_state(self) -> dict:
        """Функция читает файл с диска и возращает значение в виде словаря"""
        file = Path(self.file_path)
        file.touch(exist_ok=True)
        with open(file, "r") as json_data:
            try:
                data = json.load(json_data)
            except JSONDecodeError:
                return None
        return data


class State:
    def __init__(self, storage):
        self.storage = storage

    def is_empty(self) -> bool:
        """Функция проверяет отсутствие записей в файле состояния"""
        return self.storage.retrieve_state() is None

    def set_state(self, key: str, value: Any) -> None:
        """Функция устанавливает состояние в формате ключ-значение"""
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        """Функция получает значение по ключу"""
        if not self.is_empty():
            data = self.storage.retrieve_state()
            if key in data.keys():
                return data[key]
