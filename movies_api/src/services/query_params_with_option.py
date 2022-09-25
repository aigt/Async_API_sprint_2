import logging
import re
from typing import Any, List

from fastapi import Request
from models.request.param_with_option import ParamWithOption


def parse_param(param: str, value: Any) -> ParamWithOption:
    """Функция для поддержки квадратных скобок в имени переменных запроса.

    Args:
        param (str): Имя параметра
        value (Any): Переменная

    Returns:
        ParamWithOption: объект параметра с опцией
    """
    regex = r"(?P<param>.*)\[(?P<option>.*)\]"
    if m := re.search(regex, param):
        return ParamWithOption(
            name=m.group("param"),
            option=m.group("option"),
            value=value,
        )
    return ParamWithOption(name=param, value=value)


async def get_params_with_options(request: Request) -> List[ParamWithOption]:
    params = [parse_param(k, v) for k, v in request.query_params.items()]
    logging.debug(f'{params=}')
    return params
