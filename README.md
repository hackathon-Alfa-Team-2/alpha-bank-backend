# Хакатон+. Задача от Альфа Банка.

#### Задача: создание MVP индивидуального плана развития для сотрудников в Альфа-Банке.

Общие возможности приложения:

Руководитель может просматривать список сотрудников, добавлять индивидуальные планы развития
сотрудникам. К каждому ИПР можно добавить задачи, к каждой задаче могут оставить свои комментарии
руководитель и сотрудник.

## Использованные технологии.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
<img src ="https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
<img src="https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/>
<img src="https://img.shields.io/badge/github%20actions%20-%232671E5.svg?&style=for-the-badge&logo=github%20actions&logoColor=white"/>
<img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
<img src="https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white" />

## Установка.

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/hackathon-Alfa-Team-2/alpha-bank-backend.git
   cd alpha-bank-backend
   ```

2.
    * Создайте файл `.env` по примеру `.env.example` в папке config и заполните его.

  ```
  #Django
  DJANGO_SECRET_KEY=''
  ALLOWED_HOSTS=localhost,127.0.0.1
  CSRF_TRUSTED_ORIGINS=http://example.net/,https://example.net/
   
  # Postgres
  DB_ENGINE='django.db.backends.postgresql_psycopg2'
  POSTGRES_DB='postgres'
  POSTGRES_USER='postgres'
  POSTGRES_PASSWORD='exaple-password'
  DB_HOST=db
  DB_PORT=5432
   
  # Celery & redis
  CELERY_BROKER_REDIS_URL="redis://redis:6379/1"
   
  # Swagger docs
  BASE_REQUEST_URL=http://127.0.0.1:8000
   
  # Для автоматического создания суперпользователя
  SUPERUSER_USERNAME='superuser-username'
  SUPERUSER_PASSWORD='superuser-password'
  ```

* DJANGO_SECRET_KEY можно сгенерировать таким способом:
   ```
  python manage.py shell
  from django.core.management import utils
  utils.get_random_secret_key()
   ```

4. Из корневой дирректории выполните следующие комманды:
   ```
   cd .docker
   docker compose up -d
   ```

5. Загрузите тестовые данные в базу командой:

   ```
   docker compose exec backend python manage.py loadmockdata
   ```
6. Для доступа в админ панель используйте `SUPERUSER_USERNAME` и `SUPERUSER_PASSWORD` из .`env`
   файла.

Данные тестовых пользователей:

| Роль       | email             | password    |
|------------|-------------------|-------------|
| Supervisor | supervisor1@ya.ru | Supervisor1 |
| Supervisor | supervisor2@ya.ru | Supervisor2 |
| employee   | user3sv1@ya.ru    | User3       |
| employee   | user4sv1@ya.ru    | User4       |
| employee   | user5sv2@ya.ru    | User5       |
| employee   | user6sv1@ya.ru    | User6       |

## Наша команда разработчиков:<br>

<h4 align="left">Андрей Догадкин <a href="https://github.com/AndreyDogadkin/" target="_blank">
GitHub</a>  <a href="https://t.me/jvgger" target="_blank">  🛒</a></h4>
<h4 align="left">Андрей Пасков <a href="https://github.com/vBaMnup/">
GitHub</a>  <a href="https://t.me/vBaMnup" target="_blank">  🛒</a></h4>
<h4 align="left">Владимир
Шевченко <a href="https://github.com/vladimir-shevchenko01" target="_blank">
GitHub</a>  <a href="https://t.me/vsel_live" target="_blank">  🛒</a></h4>
<h4 align="left">Максим Коркин <a href="https://github.com/splintermax/" target="_blank">
GitHub</a></a></h4>


<div id="header" align="left">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnkzaXdvM3ZzZmJ6YnQzeGIweHdhZ2FkZjFtaDR1NWJsaDR1eTh2aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6ozomjwcQJpdz5p6/giphy.gif" width="100"/>
</div>