import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    modified: datetime
