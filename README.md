
# 📦  SUP

## 📋 Описание проекта

Этот проект является веб-приложением, разработанным с использованием **Django 5**, с поддержкой **PostgreSQL** для хранения данных, **Redis** для кэширования и очередей, а также **Celery** для асинхронных задач. Мы развертываем наш проект в изолированной среде **Docker**.

## 🛠 Стек технологий

|Технология|Описание|
|---|---|
|**Django**|Фреймворк для быстрого создания веб-приложений.|
|**PostgreSQL**|Надежная реляционная база данных для хранения данных.|
|**Redis**|Используется для кэширования и как брокер задач для Celery.|
|**Celery**|Фреймворк для управления асинхронными задачами.|
|**Docker**|Среда контейнеризации для развертывания изолированных приложений.|
|**Poetry**|Инструмент для управления зависимостями и виртуальной средой проекта.|
|**Ruff**|Быстрый линтер для проверки стиля и качества кода Python.|
|**Black**|Форматировщик кода Python, обеспечивающий единообразие стиля кода.|
|**isort**|Инструмент для упорядочивания импортов в соответствии с PEP8.|

## 🚀 Установка и настройка проекта

1. **Клонирование репозитория**:
    ```bash
    git clone https://github.com/Synt4xL4b/sup-backend-2.git
    ```
    Дальше есть такой рабочий вариант: Открываем проект в IDE. На запрос где лежит poetry можно игнорировать. Затем закрываем и снова открываем IDE. Ставим poetry в папку 
   проекта через pip. pip install poetry

   2. **Установка зависимостей**: Убедитесь, что у вас установлен `Poetry`, затем выполните:
       ```bash
       poetry install   
       ```

    
2. **Настройка переменных окружения**: создайте файл `.env` с переменными для базы данных, Redis и секретов:
    
    ```bash
    touch .env
    ```

```python
# Django settings  
DJANGO_SECRET_KEY='secret'  
DEBUG=True  
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost  
  
# Database settings  
DB_ENGINE=django.db.backends.postgresql  
POSTGRES_DB=dbname
POSTGRES_USER=pg_username  
POSTGRES_PASSWORD=pg_pass  
DB_HOST=pg_host  
DB_PORT=pg_port  
  
FRONTEND_URL=https://junov.net
```
    
4. **Запуск Docker-контейнеров**: Проект включает Docker Compose файл для запуска контейнеров с PostgreSQL, Redis и Django. Запустите контейнеры:
    
    ```bash
    env $(cat api/.env | xargs) docker-compose up -d --build
	```
        
5. **Применение миграций и создание суперпользователя**: После первого запуска, выполните миграции и создайте суперпользователя:
    
    ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
     ```
    **Если возникла проблема с миграциями, а данные хотим сохранить, можно выгрузить данные из базы и загрузить их в новую базу после миграций:**    
        
Выгрузка данных из базы в json:

```
 python -Xutf-8 manage.py dumpdata --indent=2 --output=sup_test_data.json 
```
После этого удаляем базу из контейнера:

```
docker volume rm sup_db_data
```
Повторно проводим миграции после запуска контейнеров:

Загрузка из json в базу

```
 python manage.py loaddata sup_test_data.json
```



6. **Запуск приложения локально**:
    
    
```bash
    python manage.py runserver
```    

## 🧰 Поддержка качества кода

Мы используем **Ruff**, **Black**, и **isort** для поддержания чистоты и структурированности кода. Установите **pre-commit** для проверки кода перед коммитом:

```
pre-commit install
```
    

## 📦 Дополнительные команды Docker

- **Просмотр логов**:
       
    `docker-compose logs -f`
    
- **Остановка контейнеров**:
    
    `docker-compose down`
    

## ⚙️ Запуск асинхронных задач с Celery

Для управления задачами, запустите Celery worker:

`poetry run celery -A my_project worker -l info`

## 🗄 Архитектура проекта




- .gitignore
- README.md
- api/
    - \_\_init\_\_.py
    - manage.py
    - src/
        - \_\_init\_\_.py
        - apps/
            - \_\_init\_\_.py
            - meets/
                - \_\_init\_\_.py
                - admin.py
                - apps.py
                - forms.py
                - repository.py
                - templates/
                    - create_meet_modal.html
                    - meets.html
                - tests.py
                - urls.py
                - views.py
            - projects/
                - \_\_init\_\_.py
                - admin.py
                - apps.py
                - features.py
                - forms.py
                - tags.py
                - task.py
                - tests.py
                - urls.py
                - views.py
            - users/
                - \_\_init\_\_.py
                - admin.py
                - apps.py
                - tests.py
                - views.py
        - config/
            - \_\_init\_\_.py
            - asgi.py
            - settings.py
            - urls.py
            - wsgi.py
        - db.sqlite3
        - domain/
            - custom_user/
            - meet/
                - dtos.py
                - repository.py
                - service.py
            - project/
                - dtos.py
                - repository.py
                - service.py
        - models/
            - \_\_init\_\_.py
            - apps.py
            - choice_classes.py
            - meets.py
            - migrations/
                - 0001_initial.py
                - \_\_init\_\_.py
            - projects.py
            - users.py
        - validators/
            - \_\_init\_\_.py
            - validators.py
- directory_structure.md
- generate_markdown.py
- infrasructure/
    - docker-compose.yaml
- web/
    - static/
        - css/
            - add_style.css
            - input.css
            - output.css
        - images/
        - script/
            - meets.js
            - script.js
