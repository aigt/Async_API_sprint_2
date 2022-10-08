SELECT  id,
        full_name,
        modified

FROM    content.person

WHERE   modified > %s

ORDER BY    modified

LIMIT   5000;