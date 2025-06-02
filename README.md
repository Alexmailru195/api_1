# API

### API — это Django-приложение с REST API для работы с вопросами и ответами викторины.

### Проект реализует проверку правильности ответов пользователей и интегрирован с MS SQL Server.

# Описание проекта:

## Этот проект предоставляет:

REST API для работы с категориями, вопросами и ответами.

Эндпоинт /api/quiz/check_answer/ для проверки ответов пользователя.

Аутентификацию через токены.

Поддержку загрузки данных из JSON файла.

Тестирование через unit-тесты и Postman.

# Используемые технологии:

Python 3.x

Django / Django REST Framework

MS SQL Server (через ODBC драйвер)

Token-based аутентификация

# Установка:

### Шаг 1: Клонирование репозитория:
```bash
git clone https://github.com/Alexmailru195/api_1.git 
cd api_1
```

### Шаг 2: Виртуальное окружение:
```bash
python -m venv venv
.\venv\Scripts\activate     # Windows
# source venv/bin/activate   # Linux/macOS
```
### Шаг 3: Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка базы данных:
#### Создайте файл .env в корне проекта и укажите следующие параметры:

DATABASE_NAME=
DATABASE_USER=

DATABASE_PASSWORD=

DATABASE_HOST=

DATABASE_PORT=1433

### Шаг 5: Создание базы данных:
```bash
python database_utils.py
```

### Шаг 6: Применение миграций:
```bash
python manage.py migrate
```

### Шаг 7: Загрузка данных викторины:
```bash
python manage.py load_quiz_data
```

### Шаг 8: Создание суперпользователя:
```bash
python manage.py createsuperuser
```

### Шаг 9: Запуск сервера разработки:
```bash
Шаг 9: Запуск сервера разработки
```

## Тестирование:
```bash
python manage.py test tests
```

### Ручное тестирование эндпоинта /api/quiz/check_answer/

Требования:

Активный сервер Django

Полученный токен аутентификации

Пример запроса (Postman):

Метод: POST

URL: http://localhost:8000/api/quiz/check_answer/

### Headers:

Authorization: Bearer <your_token>

Content-Type: application/json

### Тело запроса:

{
    "question_id": 1,
    "answer_id": 2
}

## Автор:

### Alexandr