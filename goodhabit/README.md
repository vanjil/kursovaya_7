# Проект GoodHabit

Этот проект представляет собой систему управления привычками с возможностью отправки уведомлений через Telegram, интеграцией с Celery для выполнения фоновых задач, а также использованием базы данных PostgreSQL и Redis. 

## Запуск проекта с помощью Docker


### Шаги для деплоя:

1. **Клонировать проект:** Склонируйте репозиторий на ваш локальный компьютер или сервер:
   
bash
   git clone https://github.com/ваш_проект_на_GitHub.git
2. Перейти в директорию проекта:
cd ваш_проект_на_GitHub
3. 
Создать файл .env: Создайте файл .env в корне проекта и заполните его 
необходимыми данными. Пример содержимого:
TELEGRAM_API_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
SECRET_KEY=ваш_django_secret_key
DEBUG=True
NAME=db_name
DB_USER=postgres
DB_PASSWORD=postgres
HOST=db
PORT=5432
REDIS_URL=redis://redis:6379/0
STRIPE_TEST_SECRET_KEY=ваш_stripe_secret_key

4.
Запуск контейнеров с Docker Compose: Соберите и запустите контейнеры, используя Docker Compose:
docker-compose up --build