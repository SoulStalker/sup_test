FROM python:3.12-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry
RUN pip install poetry

# Отключаем создание виртуального окружения в Poetry
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости проекта, включая Celery
RUN poetry install --no-interaction --no-ansi

# Копируем код проекта
COPY /api ./api

# Устанавливаем путь для Django
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app/api