from fastapi import Depends

from core.config import get_settings
from models.es_query_configs.person_list_query_config import \
    PersonListQueryConfig
from services.person.person_list_query_config import (
    person_list_query_config, person_search_query_config)

settings = get_settings()


async def _build_person_list_es_query_body(query_config: PersonListQueryConfig) -> dict:
    # Пагинация
    body = {
        'size': query_config.page.size,
        'from': (query_config.page.number - 1) * query_config.page.size,
    }

    # Добавь запрос
    if query_config.bool_q is not None:
        boolean_query = {}
        body['query'] = {'bool': boolean_query}
        # Запрос
        if query_config.bool_q.query is not None:
            boolean_query['must'] = {
                'query_string': {
                    'query': query_config.bool_q.query,
                    'fields': ['full_name'],
                },
            }

    # Выборка всех, если нет запроса или фильтрации
    body.setdefault('query', {'match_all': {}})

    return body


async def person_list_query_body(
    list_config: PersonListQueryConfig = Depends(person_list_query_config)
) -> dict:
    return await _build_person_list_es_query_body(list_config)


async def person_search_query_body(
    list_config: PersonListQueryConfig = Depends(person_search_query_config)
) -> dict:
    return await _build_person_list_es_query_body(list_config)
