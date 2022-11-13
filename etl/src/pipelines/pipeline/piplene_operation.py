from abc import ABC, abstractmethod

from pipelines.pipeline.pipeline_data import PipelineData


class PipelineOperation(ABC):
    @abstractmethod
    async def init(self) -> None:
        ...
        
    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def __call__(self, data: PipelineData) -> PipelineData:
        ...