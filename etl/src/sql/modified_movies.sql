SELECT  fw.id,
        fw.rating                   AS imdb_rating,
        ARRAY_AGG(DISTINCT g.name)  AS genre,
        fw.title,
        fw.description,

        GREATEST(
            MAX(fw.modified),
            MAX(p.modified),
            MAX(g.modified)
        ) modified,

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
        ) AS writers,
    fw.subscription


FROM        content.film_work fw

LEFT JOIN   content.person_film_work pfw
ON          pfw.film_work_id = fw.id

LEFT JOIN   content.person p
ON          p.id = pfw.person_id

LEFT JOIN   content.genre_film_work gfw
ON          gfw.film_work_id = fw.id

LEFT JOIN   content.genre g
ON          g.id = gfw.genre_id


WHERE   fw.modified > %(modified_from)s
OR      g.modified > %(modified_from)s
OR      p.modified > %(modified_from)s


GROUP BY fw.id
ORDER BY modified
LIMIT %(batch_size)s;