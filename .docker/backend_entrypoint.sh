#!/bin/sh

while pg_isready -h db -p 5432;
    do sleep 5;
    echo "Ожидание базы данных"
done;
    echo "База данных подключена"
python manage.py migrate --noinput
python manage.py collectstatic --noinput
