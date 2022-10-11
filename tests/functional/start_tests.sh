#!/bin/bash

cd /opt/app/tests/functional

pytest src/v1

exec "$@"