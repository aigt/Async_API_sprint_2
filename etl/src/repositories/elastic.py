from typing import Iterable

from elastic_transport import ApiResponse, HeadApiResponse, ObjectApiResponse
from elasticsearch import AsyncElasticsearch

from db.elastic import Elasticsearch
from models.elastic.movie import Movie


class ElastisearchRepository:
    def __init__(self, es: Elasticsearch) -> None:
        self.es = es
        self._conn: AsyncElasticsearch = None

    async def init(self) -> None:
        self._conn = await self.es.open()
        
    async def close(self) -> None:
        await self.es.close()
        self._conn = None

    async def delete_all_indeces(self) -> ObjectApiResponse:
        """Удалить все индексы.

        Returns:
            ObjectApiResponse: Ответ о выполнении операции
        """
        return await self._conn.indices.delete(index='*')

    async def create_index(self, index_name: str, schema: dict) -> ObjectApiResponse:
        """Создать индекс.

        Args:
            index_name (str): Имя индекса
            schema (dict): Схема индекса

        Returns:
            ObjectApiResponse: Ответ о выполнении операции
        """
        return await self._conn.indices.create(index=index_name, body=schema)

    def __map_filmworks_to_bulk_objects(
        self, data: Iterable[Movie], index_name: str
    ) -> list[dict]:
        """Преобразовать кинопроизведения в список формата Elasticsearch для записи

        Args:
            data (Iterable[FilmWork]): список кинопроизведений
            index_name (str): имя индекса для записи

        Returns:
            list: Подготовленный список для записи
        """
        actions = []
        for row in data:
            action = {"index": {"_index": index_name, "_id": str(row.id)}}
            doc = row.dict()
            actions.append(action)
            actions.append(doc)
        return actions

    async def bulk(self, data: Iterable[Movie], index_name: str) -> ObjectApiResponse:
        """Записать пачку кинопроизведений в индекс.

        Args:
            data (Iterable[FilmWork]): Кинопроизведения
            index_name (str): название индекса

        Returns:
            ObjectApiResponse: Ответ о выполнении операции
        """
        prepared_data = self.__map_filmworks_to_bulk_objects(data, index_name)
        return await self._conn.bulk(index=index_name, operations=prepared_data)

    async def put(self, item: Movie, index_name: str) -> ObjectApiResponse:
        """Положить одно кинопроизведение в индекс

        Args:
            item (FilmWork): кинопроизведение
            index_name (str): название индекса

        Returns:
            ObjectApiResponse: Ответ о выполнении операции
        """
        return await self._conn.index(index=index_name, body=item.json())

    async def index_exists(self, index_name: str) -> HeadApiResponse:
        """Проверить существует ли индекс.

        Args:
            index_name (str): Название индекса

        Returns:
            HeadApiResponse: True, если существует
        """
        return await self._conn.indices.exists(index=index_name)

    async def create_index_if_not_exists(self, index_name: str, schema: dict) -> ApiResponse:
        """Создать индекс, если не существует.

        Args:
            index_name (str): Имя индекса
            schema (dict): Схема индекса

        Returns:
            ApiResponse: True, если существует, иначе ответ о выполнении операции
        """
        if exists_resp := await self.index_exists(index_name):
            return exists_resp
        else:
            return await self.create_index(
                index_name=index_name,
                schema=schema,
            )
