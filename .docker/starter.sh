#!/bin/sh

while pg_isready -h db -p 5432; do
    sleep 5
    echo "Ожидание базы данных"
done
echo "База данных подключена"

echo "_____________Выполняем миграции_________________"
python manage.py migrate
echo "_____________Собираем статику_________________"
python manage.py collectstatic --noinput
python manage.py loadmockdata
