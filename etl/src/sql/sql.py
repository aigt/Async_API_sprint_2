def load_sql(filename: str) -> str:
    with open(filename, encoding='utf-8') as query_file:
        query = query_file.read()
    return query


extract_queries = {
    "get_modified_movies": load_sql('sql/modified_movies.sql'),
    "get_all_genres": load_sql('sql/all_genres.sql'),
    "get_all_persons": load_sql('sql/all_persons.sql'),
}
