# Backend Dockerfile для LRA-26
FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements/base.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]