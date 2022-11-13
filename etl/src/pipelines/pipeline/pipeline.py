from pipelines.pipeline.pipeline_data import PipelineData
from pipelines.pipeline.piplene_operation import PipelineOperation
from states.state import State


class Pipeline:
    def __init__(
        self, *,
        extract: PipelineOperation,
        transform_function: PipelineOperation,
        load_function: PipelineOperation,
        state: State,
    ) -> None:
        self.extract = extract
        self.transform = transform_function
        self.load = load_function
        self.state = state
    
    async def run(self):
        data = PipelineData()
        
        await self.extract.init()
        await self.transform.init()
        await self.load.init()
        
        while True:
            data = await self._pipeline(data)
            if data.items is None:
                break
            self.state.set_state(key="modified", value=data.modified_from)
        
        await self.extract.close()
        await self.transform.close()
        await self.load.close()

    async def _pipeline(self, data: PipelineData) -> PipelineData:
        data = await self.extract(data)
        if data.items is None:
            return data
        data = await self.transform(data)
        data = await self.load(data)
        return data
    
    
