from fastapi import Depends

from core.config import get_settings
from models.es_query_configs.film_list_query_config import FilmListQueryConfig
from services.film.film_list_query_config import (film_list_query_config,
                                                  film_search_query_config)

settings = get_settings()


async def _build_film_list_es_query_body(query_config: FilmListQueryConfig) -> dict:
    # Пагинация
    body = {
        'size': query_config.page.size,
        'from': (query_config.page.number - 1) * query_config.page.size,
    }

    # Добавь сортировку, если требуется
    if query_config.sort is not None:
        body['sort'] = {
            query_config.sort.field: {
                'order': query_config.sort.order,
            },
        }

    # Добавь запрос и/или фильтрацию
    if query_config.bool_q is not None:
        boolean_query = {}
        body['query'] = {'bool': boolean_query}
        # Фильтрация
        if query_config.bool_q.filter is not None:
            # Выбор по какому полю фильтровать
            match query_config.bool_q.filter.field:
                case 'genre':
                    boolean_query['filter'] = {
                        'match': {'genre': query_config.bool_q.filter.value},
                    }
        # Запрос
        if query_config.bool_q.query is not None:
            boolean_query['must'] = {
                'query_string': {
                    'query': query_config.bool_q.query,
                    'fields': ['title', 'description'],
                },
            }

    # Выборка всех, если нет запроса или фильтрации
    body.setdefault('query', {'match_all': {}})

    return body


async def film_list_query_body(
    list_config: FilmListQueryConfig = Depends(film_list_query_config)
) -> dict:
    return await _build_film_list_es_query_body(list_config)
    

async def film_search_query_body(
    list_config: FilmListQueryConfig = Depends(film_search_query_config)
) -> dict:
    return await _build_film_list_es_query_body(list_config)
