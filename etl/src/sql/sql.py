extract_queries = {
    "get_persons_id": """SELECT id, modified
FROM content.person
WHERE modified > %s
ORDER BY modified
LIMIT 200; 
""",
    "get_genres_id": """SELECT id, modified
FROM content.genre
WHERE modified > %s
ORDER BY modified
LIMIT 200; 
""",
    "get_movies_id_with_modified_persons": """ SELECT fw.id
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
WHERE pfw.person_id IN %s
ORDER BY fw.modified
LIMIT 200;
""",
    "get_movies_id_with_modified_genres": """ SELECT fw.id
FROM content.film_work fw
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
WHERE gfw.genre_id IN %s
ORDER BY fw.modified
LIMIT 200;
""",
    "get_modified_movies": """ SELECT
    fw.id,
    fw.rating AS imdb_rating,
    ARRAY_AGG(DISTINCT g.name) AS genre,
    fw.title,
    fw.description,
    fw.modified,
    COALESCE (
        STRING_AGG(DISTINCT p.full_name, ', ')
        FILTER (WHERE pfw.role = 'director'), ''
    ) AS director,
    COALESCE (
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER (WHERE pfw.role = 'actor')
    ) AS actors_names,
    COALESCE (
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER (WHERE pfw.role = 'writer')
    ) AS writers_names,
    COALESCE (
        JSON_AGG(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE pfw.role = 'actor'),
        '[]'
    ) AS actors,
    COALESCE (
        JSON_AGG(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE pfw.role = 'writer'),
        '[]'
    ) AS writers
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.modified > %s
    GROUP BY fw.id
    ORDER BY fw.modified
    LIMIT 200;
    """,
    "get_movies_with_modified_persons_or_genres": """ SELECT
    fw.id,
    fw.rating AS imdb_rating,
    ARRAY_AGG(DISTINCT g.name) AS genre,
    fw.title,
    fw.description,
    fw.modified,
    COALESCE (
        STRING_AGG(DISTINCT p.full_name, ', ')
        FILTER (WHERE pfw.role = 'director'), ''
    ) AS director,
    COALESCE (
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER (WHERE pfw.role = 'actor')
    ) AS actors_names,
    COALESCE (
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER (WHERE pfw.role = 'writer')
    ) AS writers_names,
    COALESCE (
        JSON_AGG(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE pfw.role = 'actor'),
        '[]'
    ) AS actors,
    COALESCE (
        JSON_AGG(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE pfw.role = 'writer'),
        '[]'
    ) AS writers
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.id IN %s
    GROUP BY fw.id
    ORDER BY fw.modified
    LIMIT 200;
""",
    "get_all_genres": """SELECT id, name, modified
FROM content.genre
WHERE modified > %s
ORDER BY modified
LIMIT 200; 
""",
    "get_all_persons": """SELECT id, full_name, modified
FROM content.person
WHERE modified > %s
ORDER BY modified
LIMIT 200; 
""",
}
