from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> Any:
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class OrjsonModel(BaseModel):
    """Базовый класс для pydantic-моделей c orjson-сериализацией."""

    class Config:
        json_loads = orjson.loads
        json_dumbs = orjson_dumps
