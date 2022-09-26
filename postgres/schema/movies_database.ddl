CREATE SCHEMA IF NOT EXISTS content;
CREATE SCHEMA IF NOT EXISTS public;



CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type VARCHAR(20) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    CONSTRAINT unique_film_with_date UNIQUE (creation_date, title)
); 



CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone,
    UNIQUE (name)
);



CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone   
);



CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid NOT NULL,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);



CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid NOT NULL,
    person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL,
    created timestamp with time zone
);



CREATE INDEX IF NOT EXISTS date_and_rating 
ON content.film_work (creation_date, rating, title);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person 
ON content.person_film_work (film_work_id, person_id, role);

CREATE UNIQUE INDEX IF NOT EXISTS film_genre
ON content.genre_film_work (film_work_id, genre_id);



-- Индексы на modified для поиска ETL

CREATE INDEX IF NOT EXISTS genre_modified_idx
ON content.genre (modified);

CREATE INDEX IF NOT EXISTS film_work_modified_idx
ON content.film_work (modified);

CREATE INDEX IF NOT EXISTS person_modified_idx
ON content.person (modified);