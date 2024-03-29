import logging
from dataclasses import asdict
from typing import Any

from elasticsearch import Elasticsearch
from decorators.es_reconnect import es_reconnect


class ElasticLoader:
    """Импорт данных в ElasticSearch"""

    def __init__(
        self,
        index: str,
        settings: dict,
        mappings: dict,
        state: Any,
        conn: str = "http://elasticsearch:9200",
    ) -> None:
        self._conn = conn
        self._connection = None
        self.index = index
        self.settings = settings
        self.mappings = mappings
        self.state = state

    def connected(self) -> bool:
        """Функция проверяет наличие соединения с БД"""
        return self._connection and self._connection.ping()

    def reconnect(self):
        """Функция закрывает соединение с БД и создает новое"""
        self.close()
        self._connection = Elasticsearch(self._conn)

    def close(self) -> None:
        """Функция закрывает соединение с БД"""
        if self.connected():
            try:
                self._connection.transport.close()
            except Exception as e:
                logging.error(e)
        self._connection = None

    @es_reconnect
    def load(self, dataclass_data: list) -> None:
        """Функция загружает полученные данные в ElasticSearch.
        При необходимости создает индекс.
        В зависимости от id документы либо создаются, либо обновляются"""
        if not self._connection.indices.exists(index=self.index['movies']):
            self._connection.indices.create(
                index=self.index['movies'],
                settings=self.settings,
                mappings=self.mappings['movies'],
            )
        if not self._connection.indices.exists(index=self.index['genres']):
            self._connection.indices.create(
                index=self.index['genres'],
                settings=self.settings,
                mappings=self.mappings['genres'],
            )
        if not self._connection.indices.exists(index=self.index['persons_v2']):
            self._connection.indices.create(
                index=self.index['persons_v2'],
                settings=self.settings,
                mappings=self.mappings['persons_v2'],
            )

        if dataclass_data[0]:
            row_count = len(dataclass_data[0])
            for number in range(row_count):
                doc_id = dataclass_data[0][number].id
                doc_data = asdict(dataclass_data[0][number])
                modified_data = doc_data.pop("modified")

                if self._connection.exists(index=self.index['movies'], id=doc_id):
                    updated_data = doc_data

                    self._connection.update(
                        index=self.index['movies'],
                        body={"doc": updated_data},
                        id=doc_id,
                    )
                    logging.info(f"document {doc_id} was updated.")
                else:
                    self._connection.create(
                        index=self.index['movies'],
                        document=doc_data,
                        id=doc_id,
                    )
                    logging.info(f"document {doc_id} was created.")
            self.state["movie"].set_state(key="modified", value=modified_data)

        if dataclass_data[1]:
            row_count = len(dataclass_data[1])
            for number in range(row_count):
                doc_id = dataclass_data[1][number].id
                doc_data = asdict(dataclass_data[1][number])
                modified_data = doc_data.pop("modified")

                if self._connection.exists(index=self.index['genres'], id=doc_id):
                    updated_data = doc_data

                    self._connection.update(
                        index=self.index['genres'],
                        body={"doc": updated_data},
                        id=doc_id,
                    )
                    logging.info(f"document {doc_id} was updated.")
                else:
                    self._connection.create(
                        index=self.index['genres'],
                        document=doc_data,
                        id=doc_id,
                    )
                    logging.info(f"document {doc_id} was created.")
            self.state["all_genres"].set_state(key="modified", value=modified_data)

        if dataclass_data[2]:
            row_count = len(dataclass_data[2])
            for number in range(row_count):
                doc_id = dataclass_data[2][number].id
                doc_data = dataclass_data[2][number].dict()
                modified_data = doc_data.pop("modified")

                if self._connection.exists(index=self.index['persons_v2'], id=doc_id):
                    updated_data = doc_data

                    self._connection.update(
                        index=self.index['persons_v2'],
                        body={"doc": updated_data},
                        id=doc_id,
                    )
                    logging.info(f"document {doc_id} was updated.")
                else:
                    self._connection.create(
                        index=self.index['persons_v2'],
                        document=doc_data,
                        id=doc_id,
                    )
                    logging.info(f"document {doc_id} was created.")
            self.state["all_persons"].set_state(key="modified", value=modified_data)

        if not dataclass_data[0] and not dataclass_data[1] and not dataclass_data[2]:
            logging.info("No new data in Postgres")
