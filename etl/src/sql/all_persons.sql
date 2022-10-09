SELECT  p.id,
        p.full_name,

        GREATEST(
            MAX(fw.modified),
            MAX(p.modified)
        ) modified,

        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'role', pfw.role,
                    'film_id', pfw.film_work_id,
                    'film_title', fw.title,
                    'film_imdb_rating', fw.rating
                )
                ) FILTER (WHERE fw.id IS NOT NULL),
            '[]'
        ) AS roles


FROM        content.person p

LEFT JOIN   content.person_film_work pfw
ON          pfw.person_id = p.id

LEFT JOIN   content.film_work fw
ON          fw.id = pfw.film_work_id


WHERE       p.modified >  %(modified_from)s
OR          fw.modified > %(modified_from)s

GROUP BY    p.id
ORDER BY    modified
LIMIT       %(batch_size)s;