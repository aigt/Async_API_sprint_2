from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel


class PipelineData(BaseModel):
    items: list[Any] | None = None
    modified_from: datetime = datetime.min.replace(tzinfo=ZoneInfo(key='Etc/UTC'))
    modified_to: datetime = datetime.min.replace(tzinfo=ZoneInfo(key='Etc/UTC'))