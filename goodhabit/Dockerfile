# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y libpq-dev gcc

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем необходимые зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Добавляем команду для запуска сервера Django по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
