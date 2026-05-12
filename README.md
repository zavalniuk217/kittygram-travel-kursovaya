# 🐱 Kittygram API | Wishlist нужд кота

Kittygram — это REST API для управления котиками и их достижениями с расширенной функциональностью для формирования и отслеживания списка потребностей питомца (Wishlist). Проект разработан в рамках курсовой работы по дисциплине "Интеграция и управление приложениями на удаленном сервере".

## Технологический стек

- Язык: Python 3.10+
- Фреймворк: Django 3.2 + Django REST Framework 3.12
- Аутентификация: Djoser (JWT + Bearer Token)
- База данных: PostgreSQL (в Docker) / SQLite (локально)
- Документация: Browsable API (DRF)

## Запуск через Docker (рекомендуемый способ)

### 1. Клонирование репозитория

git clone https://github.com/zavalniuk217/kittygram-travel-kursovaya.git
cd kittygram-travel-kursovaya

### 2. Настройка переменных окружения

cp .env.example .env

### 3. Запуск проекта

docker-compose up --build

### 4. Создание суперпользователя (опционально)

docker-compose exec web python manage.py createsuperuser

Проект будет доступен по адресу: http://localhost:8000/

## Как запустить проект (локально без Docker)

### 1. Клонирование репозитория

git clone https://github.com/zavalniuk217/kittygram-travel-kursovaya.git
cd kittygram-travel-kursovaya

### 2. Создание и активация виртуального окружения

Windows:
python -m venv env
env\Scripts\activate

Linux / macOS:
python3 -m venv env
source env/bin/activate

### 3. Установка зависимостей

pip install --upgrade pip
pip install -r requirements.txt

### 4. Настройка переменных окружения

Создайте файл .env в корне проекта:
SECRET_KEY=django-secure-wallet-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

### 5. Выполнение миграций и запуск

python manage.py migrate
python manage.py runserver

Проект будет доступен по адресу: http://127.0.0.1:8000/

## Основные эндпоинты API

POST /auth/users/ - Регистрация пользователя

POST /auth/jwt/create/ - Получение JWT-токена

GET /cats/ - Список всех котиков

POST /cats/ - Добавить котика (требуется токен)

GET /cats/{id}/ - Получить котика по ID

PATCH /cats/{id}/ - Изменить котика (только владелец)

DELETE /cats/{id}/ - Удалить котика (только владелец)

GET /achievements/ - Список достижений

GET /api/travel/routes/ - Список маршрутов путешествий

POST /api/travel/routes/ - Создать маршрут (требуется токен)

GET /api/travel/routes/{id}/ - Получить маршрут по ID

PATCH /api/travel/routes/{id}/ - Изменить маршрут (только владелец)

DELETE /api/travel/routes/{id}/ - Удалить маршрут (только владелец)

POST /api/travel/routes/{id}/join/ - Присоединиться к маршруту (требуется токен)

POST /api/travel/routes/{id}/leave/ - Отменить участие в маршруте (требуется токен)

POST /api/travel/routes/{id}/points/ - Добавить промежуточную точку маршрута (только владелец)

## Примеры запросов

Регистрация:
{"username": "kotik_lover", "password": "securepass123"}

Получение токена:
{"username": "kotik_lover", "password": "securepass123"}

Создание котика (заголовок: Authorization: Bearer <токен>):
{"name": "Барсик", "color": "white", "birth_year": 2020, "owner": 1, "achievements": [{"achievement_name": "лучший кот"}]}

Создание маршрута (заголовок: Authorization: Bearer <токен>):
{"title": "Путешествие в Сочи", "start_date": "2026-07-01", "end_date": "2026-07-10", "start_city": "Москва", "end_city": "Сочи", "cats": [1]}

Присоединение к маршруту (заголовок: Authorization: Bearer <токен>):
{}

Ответ сервера:
{"id": 1, "title": "Путешествие в Сочи", "author_username": "admin2", "start_city": "Москва", "end_city": "Сочи", "start_date": "2026-07-01", "end_date": "2026-07-10", "bookings_count": 1}

## Безопасность и валидация

- JWT-аутентификация: доступ только для авторизованных
- Права владельца: только создатель может редактировать/удалять
- Валидация года рождения: нельзя указать год в будущем
- Валидация дат маршрута: дата окончания не может быть раньше даты начала
- Нельзя присоединиться к своему собственному маршруту
- Цвет выбирается из списка (Gray, Black, White, Ginger, Mixed)

## Документация

После запуска: http://127.0.0.1:8000/cats/ и http://127.0.0.1:8000/api/travel/routes/

## Разработчик

Студент: Завальнюк Е. А.
Группа: ПИЭУ/246
Год: 2026
