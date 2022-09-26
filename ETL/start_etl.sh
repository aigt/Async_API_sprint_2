#!/bin/bash

cd /opt/app/

# Перезапускай проверку/выполнение задач etl через каждые 15 мин
while :
do
    python etl.py
    sleep 15m
done

exec "$@"
