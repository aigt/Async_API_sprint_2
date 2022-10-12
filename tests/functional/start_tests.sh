#!/bin/bash

cd /opt/app/tests/functional

pytest .

exec "$@"