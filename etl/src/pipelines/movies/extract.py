from datetime import datetime

from psycopg.rows import class_row

from db.postgres import Postgres
from models.postgres.movie import Movie
from pipelines.pipeline.pipeline_data import PipelineData
from pipelines.pipeline.piplene_operation import PipelineOperation


class Extract(PipelineOperation):
    def __init__(self, postgres: Postgres, batch_size: int, query: str) -> None:
        self.postgres = postgres
        self.batch_size = batch_size
        self.query = query
        
    async def init(self) -> None:
        await self.postgres.open()
        
    async def close(self) -> None:
        await self.postgres.close()

    async def __call__(self, data: PipelineData) -> PipelineData:
        """
        Запустить извлечение данных.

        :param data: входные данные
        :return: извлечённые данные
        """
        movies = await self._fetch(data.last_modified)
        movies = self.fix_modified_to_collisions(movies)
        
        if not movies:
            return PipelineData(
                items=None,
                modified_from=data.modified_from,
                modified_to=data.modified_to,
            )
        
        modified_from = data.modified_to
        modified_to = max(x.modified for x in movies)
        
        return PipelineData(
            items=movies,
            modified_from=modified_from,
            modified_to=modified_to,
        )

    async def _fetch(self, modified_from: datetime) -> list[Movie]:
        """
        Получить данные из БД.

        :param modified_from: дата модификации после которой извлеч данные
        :return: извлечённый список
        """
        query_vars = {
            'batch_size': self.batch_size,
            'modified_from': modified_from,
        }
        async with self.postgres.connection() as conn:
            async with conn.cursor() as cursor:
                cursor.row_factory = class_row(Movie)
                await cursor.execute(self.query, query_vars)
                return await cursor.fetchall()

    @classmethod
    def fix_modified_to_collisions(items: list[Movie] | None) -> list[Movie]:
        """
        Исправление коллизий максимального значения modified.
        
        Функция отсекает элементы с максимальным modified, до тех пор пока они
        равны предыдущему.

        :param items: список для обработки
        :return: список без коллизий
        """
        if not items:
            return items
        
        res = sorted(items, key=lambda item: item.modified)
        while True:
            if len(res) == 1:
                return res
            
            end_item = res[-1]
            res = res[0:-1]
            
            if res[-1] != end_item:
                return res
