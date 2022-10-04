#!/bin/bash

set -e

echo "########################################################################"

echo "Apply movies schema to postgres db"
psql -U ${POSTGRES_USER:-app} -d ${POSTGRES_DB:-postgres} -f /movies/schema/movies_database.ddl

echo "Load movies db dump"
psql -U ${POSTGRES_USER:-app} -d ${POSTGRES_DB:-postgres} < /movies/dump/movies_db_dump.sql
