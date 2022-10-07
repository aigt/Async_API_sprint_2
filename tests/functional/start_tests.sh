#!/bin/bash

cd /opt/app/

pytest

exec "$@"