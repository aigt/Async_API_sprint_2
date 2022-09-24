#!/bin/bash

set -e

psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/db_init/movies_database.ddl

psql -U postgres -d postgres < /docker-entrypoint-initdb.d/db_init/movies_db_dump.sql

