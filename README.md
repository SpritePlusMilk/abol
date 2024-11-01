# Тестовое задание для "Аболъ", Мусин Рим
### Структура репозтория

Директории:
- api - Django-приложение, реализующее REST API;
- env - демонстрационные файлы с переменными окружения: **.db-env** - переменные для БД, **.mq-env** - переменные для работы с RabbitMQ, **.project-env** - переменные для Django проекта;
- image_processing - содержит скрипт, реализующий функциональность сервиса, прослушивающего брокер сообщений и логирующего сообщения. Развёртывается в отдельном контейнере;
- nginx - Docker-файл и файл конфигурации для вэб-сервера nginx;
- project - корневая папка Django-проекта;
- supervisor - файлы для конфигурации supervisorctl, необходимы для запуска Celery (демонизация).

Файлы:
- .coveragerc - файл для настройки для pytest-cov; 
- docker-compose.yml - общий файл для сборки и деплоя всех составных проекта;
- Dockerfile - Docker-файл Django-проекта;
- pytest.ini - файл настроек для pytest;
- ruff.toml - файл конфигурации для линтера ruff;
- requirements.txt - перечень используемых Python-библиотек.

### Краткая информация об использованных средствах
- Для реализации REST API был использован Django REST Framework;
- Для автогенерации документации API задействован drf-spectacular (SwaggerUI/Redoc);
- В качестве брокера сообщений используется RabbitMQ (с помощью библиотеки Pika), сервис для логирования сообщений из брокера реализован в виде небольшого скрипта, в котором реализованы повторные попытки подключения к брокеру с помощью retry;
- Для выполнения фоновой обработки загружаемых изображений используется Celery, запускаемая с помощью supervisorctl;
- Для деплоя использован вэб-сервер Nginx в связке с Gunicorn;
- В качестве линтера и форматтера кода выбран Ruff;
- Pytest для 'прогона тестов' и получения информации о покрытии. В рамках тестов задействованы Faker и Factory-boy для генерации данных;
- База данных Postgresql;
- Для кэширования использован Django-redis;
- Для настройки получения статики (например, в админ-панели и SwaggerUI) выбран WhiteNoise;
- Механизм авторизации с помощью JWT-токента реализуется библиотекой Djangorestframework-simplejwt


## Запуск проекта
В директории репозитория ввести в консоли:
- `docker-compose build`
- `docker-compose up -d`

После запуска контейнеров проверить работоспособность перейдя по адресу: http://127.0.0.1/

В случае, если миграции не применились использовать:
- `docker exec -ti abol-web-1 python manage.py migrate --noinput`

## ENV

.db-env
* DB_ENGINE=django.db.backends.postgresql_psycopg2
* POSTGRES_USER=testuser
* POSTGRES_DB=testdb
* POSTGRES_PASSWORD=password
* POSTGRES_HOST=postgres
* POSTGRES_PORT=5432
* PGDATA=/var/lib/postgresql/data/
* C_FORCE_ROOT=true

.project-env
* DEBUG = 1
* ALLOWED_HOSTS = 127.0.0.1 localhost [::1]
* SECRET_KEY = django-insecure-6lpxm23l!*9q2froel8$+&^^1fgca3k2t7kj*5)s**89s10d7e

.mq-env
* MQ_HOST = rabbitmq
* MQ_PORT = 5672
* MQ_USER = guest
* MQ_PASS = guest
* MQ_ROUTING_KEY = messages

