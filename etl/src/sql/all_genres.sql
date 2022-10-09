SELECT  id,
        name,
        modified

FROM    content.genre

WHERE   modified > %(modified_from)s

ORDER BY    modified

LIMIT   %(batch_size)s;