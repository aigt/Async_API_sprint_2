#!/bin/bash

cd /opt/app/

python etl.py

exec "$@"
