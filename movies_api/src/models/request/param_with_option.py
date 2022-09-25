from typing import Any

from pydantic import BaseModel


class ParamWithOption(BaseModel):
    """Объект параметра с опцией.

    Например, приходящий в строке filter[genres]=horror
    """

    name: str
    option: str | None
    value: Any | None
