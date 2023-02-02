# Проект museum_news.
***
Проект museum_news служит для сбора новостей с сайтов музеев.
***

## Возможности.

* Проверка сайтов, указанных в файле .CSV на то, что они созданы на wordpress.
* Запрос с таких сайтов новостей и сохранение их в БД.
* Сбор новостей реализован в отдельном процессе с помощью Celery.
* Получение через API новостей из БД с возможностью поиска по заголовкам и тексту новости.
***
***
После запуска через docker-compose необходимо создать БД (если еще нет) с именем указанным в переменной окружения DB_NAME
и настроить доступ к ней для пользователя указанного в переменной POSTGRES_USER:
```
docker exec -t -i yourdbcontainernumber bash
psql -U 'POSTGRES_USER'
CREATE DATABASE 'DB_NAME';
GRANT ALL PRIVILEGES ON DATABASE 'DB_NAME' TO 'POSTGRES_USER';
```
***
После этого необходимо выполнить миграции в контейнере web:
```docker exec -t -i yourdbcontainernumber bash```
Перейти в папку с ```manage.py``` и выполнить 
```python3 manage.py migrate``` и ```python3 manage.py createsuperuser```

Переменные окружения, необходимые для запуска:

* DB_ENGINE - настройка ENGINE для БД в django.settings
* DB_HOST - имя хоста с БД (в проекте - 'db')
* DB_NAME - имя БД (в проекте - 'postgres')
* DB_PORT - порт для БД
* POSTGRES_PASSWORD - пароль БД
* POSTGRES_USER - пользователь БД
* DJANGO_SECRET_KEY - ключ для django проекта
* CELERY_BROKER - сервер redis
* CELERY_BACKEND - сервер redis

Данные переменные необходимо сохранить в файле ```.env```в каталоге с manage.py
***
Примеры запросов:
* GET http://127.0.0.1:8000/api/news/?q=TEST - поиск по новостям
* GET http://127.0.0.1:8000/api/news/ - выдать все новости из БД
* GET http://127.0.0.1:8000/api/collect/ - начать сбор новостей с сайтов
***
Предложения, замечания, ограничения:
Сбор выполняется долго (~1 час), но в отдельном процессе, поэтому приложение не блокируется.
Возможно сделать задачу сбора автономной и цикличной вместо запуска по запросу.

***
Автор:
* Рогозов Михаил