import logging
from typing import Any

import psycopg2
from psycopg2.extras import DictCursor

from decorators.pg_reconnect import pg_reconnect


class PostgresExtractor:
    """Извлечение данных из Postgres"""

    def __init__(self, dsn, query: str, state: Any) -> None:
        self.query = query
        self.state = state
        self._dsn = dsn
        self._connection = None

    def connected(self) -> bool:
        """Функция проверяет наличие соединения с БД"""
        return self._connection and self._connection.closed is not None

    def reconnect(self) -> None:
        """Функция закрывает соединение с БД и создает новое"""
        self.close()
        self._connection = psycopg2.connect(dsn=self._dsn)

    def close(self) -> None:
        """Функция закрывает соединение с БД"""
        if self.connected():
            try:
                self._connection.close()
            except Exception as e:
                logging.error(e)
        self._connection = None

    def get_movies_changes(self, cursor, query, state) -> list:
        if state.is_empty():
            last_modified = "1000-01-01 00:00:00.222397+00"
        else:
            last_modified = state.get_state("modified")
            
        cursor.execute(
            query,
            {
                'batch_size': 1000,
                'modified_from': last_modified,
            },
        )
        
        data = cursor.fetchall()
        if data:
            modified = data[len(data) - 1]["modified"]
            self.movie_modified = modified
            return data
        return []

    def get_all_genres_persons(self, cursor, query, state) -> list:
        if state.is_empty():
            last_modified = "1000-01-01 00:00:00.222397+00"
        else:
            last_modified = state.get_state("modified")

        cursor.execute(
            query,
            {
                'batch_size': 5000,
                'modified_from': last_modified,
            },
        )
        data = cursor.fetchall()
        if data:
            modified = data[len(data) - 1]["modified"]
            state.set_state(key="modified", value=modified)
            return data
        return data

    @pg_reconnect
    def extract(self) -> list:
        """Функция подключается к БД, выполняет запрос и возвращает данные в виде списка"""
        data = []

        pg_curs = self._connection.cursor(cursor_factory=DictCursor)

        data += self.get_movies_changes(
            cursor=pg_curs,
            query=self.query["get_modified_movies"],
            state=self.state["movie"],
        )

        genres_data = self.get_all_genres_persons(
            cursor=pg_curs,
            query=self.query["get_all_genres"],
            state=self.state["all_genres"],
        )

        persons_data = self.get_all_genres_persons(
            cursor=pg_curs,
            query=self.query["get_all_persons"],
            state=self.state["all_persons"],
        )

        return (data, genres_data, persons_data)
