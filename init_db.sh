#!/bin/bash

set -e

psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/postgres/movies_database.ddl

psql -U postgres -d postgres < /docker-entrypoint-initdb.d/postgres/movies_db_dump.sql

