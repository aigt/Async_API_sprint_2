from logging import config as logging_config

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.api import api_router
from core.config import get_settings
from core.logger import LOGGING
from db import elastic, redis

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

settings = get_settings()

description = """
Асинхронный API для кинотеатра

## Основные сущности

* Фильм
* Жанр
* Персоны:
  * Актёр
  * Режиссёр
  * Сценарист
"""

tags_metadata = [
    {
        "name": "films",
        "description": "Операции с фильмами.",
    },
    {
        "name": "genres",
        "description": "Операции с жанрами.",
    },
    {
        "name": "persons",
        "description": "Операции с персонами (в т.ч. актёрами, режиссёрами, сценаристами).",
    },
]


app = FastAPI(
    title=settings.project_name,
    description=description,
    openapi_tags=tags_metadata,
    version="1.0.0",
    docs_url='/api/openapi',
    contact={
        "name": "Ссылка на репозиторий GitHub",
        "url": "https://github.com/aigt/Async_API_sprint_1",
    },
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.Redis.from_url(settings.redis_dsn)
    elastic.es = AsyncElasticsearch(
        hosts=[f'http://{settings.elastic_host}:{settings.elastic_port}']
    )


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


# Подключаем роутер к серверу
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
