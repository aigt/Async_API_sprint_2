"""Модуль работы с БД postgres."""
import asyncio
import signal
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

import psycopg
from psycopg import AsyncConnection


class Postgres:
    """Контекстный менеджер postgres."""

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.conn: AsyncConnection[Any] = None
        
        # If the query is running in an async connection, a Ctrl-C will be likely
        # intercepted by the async loop and interrupt the whole program. In order
        # to emulate what normally happens with blocking connections, we use
        # asyncio’s add_signal_handler(), to call Connection.cancel()
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.close)

    def cancel(self) -> None:
        if self.conn is not None:
            self.conn.cancel()
        
    async def open(self) -> None:
        self.conn = await psycopg.AsyncConnection.connect(self.dsn)
        
    async def close(self) -> None:
        if self.conn is None:
            return
        await self.conn.close()
        self.conn = None

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[AsyncConnection[Any]]:
        """Контекстный менеджер для соединения с postgres."""
        try:
            yield self.conn
        except BaseException:
            await self.conn.rollback()
            await self.close()
        else:
            await self.conn.commit()
