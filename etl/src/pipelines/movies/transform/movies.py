from models.elastic.movie import Movie, Person
from models.postgres.movie import Movie as ExtractedMovie
from pipelines.pipeline.pipeline_data import PipelineData
from pipelines.pipeline.piplene_operation import PipelineOperation


class TransformMovies(PipelineOperation):
    def __init__(self) -> None:
        pass

    async def init(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def __call__(self, data: PipelineData) -> PipelineData:
        e_movies: list[ExtractedMovie] = data.items
        return PipelineData(
            items =[
                Movie(
                    id=movie.id,
                    imdb_rating=movie.imdb_rating,
                    genre=movie.genre,
                    title=movie.title,
                    description=movie.description,
                    director=movie.director,
                    actors_names=movie.actors_names,
                    writers_names=movie.writers_names,
                    actors=[
                        Person(
                            id=actor.id,
                            name=actor.name,
                        )
                        for actor in movie.actors
                    ],
                    writers=[
                        Person(
                            id=writer.id,
                            name=writer.name,
                        )
                        for writer in movie.writers
                    ],
                )
                for movie in e_movies
            ],
            modified_from=data.modified_from,
            modified_to=data.modified_to,
        )