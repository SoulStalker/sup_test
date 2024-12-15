FROM python:3.12-slim

WORKDIR /app

RUN apt-get update

COPY pyproject.toml poetry.lock ./

RUN #pip install --upgrade pip
RUN pip install poetry
# Устанавливаем зависимости
RUN poetry install

# Копируем папку api в контейнер
RUN mkdir api
COPY /api ./api

# Указываем путь к локально установленным пакетам (если это нужно)
ENV PATH="/root/.local/bin:$PATH"

CMD ["celery", "--app=api.src.services.celery", "worker", "--loglevel=info"]

# Указываем рабочую директорию для Django
WORKDIR /app/api

# Команда для запуска сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
