import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    modified: datetime
