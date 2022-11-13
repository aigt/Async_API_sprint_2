from contextlib import asynccontextmanager
from typing import AsyncIterator

from elasticsearch import AsyncElasticsearch


class Elasticsearch:
    """Контекстный менеджер Elasticsearch."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.es: AsyncElasticsearch = None

    async def open(self) -> None:
        self.es = AsyncElasticsearch(hosts=[self.url])
        return self.es

    async def close(self) -> None:
        if self.es is None:
            return
        await self.es.close()
        self.es = None
