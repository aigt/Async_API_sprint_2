from models.elastic.movie import Movie, Person
from pipelines.pipeline.pipeline_data import PipelineData
from pipelines.pipeline.piplene_operation import PipelineOperation
from repositories.elastic import ElastisearchRepository


class Load(PipelineOperation):
    def __init__(
        self,
        repo: ElastisearchRepository,
        index_name: str,
        index_schema: dict
    ) -> None:
        self.repo = repo
        self.index_name = index_name
        self.index_schema = index_schema
        
    async def init(self) -> None:
        await self.repo.init()
        
    async def close(self) -> None:
        await self.repo.close()

    async def __call__(self, data: PipelineData) -> PipelineData:
        movies: list[Movie] = data.items
        await self.repo.create_index_if_not_exists(self.index_name, self.index_schema)
        await self.repo.bulk(movies, self.index_name)
        return PipelineData(
            items=None,
            modified_from=data.modified_to,
        )


