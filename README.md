# API для Yatube

## Описание
REST API для социальной сети Yatube. Позволяет создавать посты, комментарии, подписываться на авторов. Использует JWT-аутентификацию.

## Установка
Клонировать репозиторий и перейти в него в командной строке:
git clone https://github.com/yandex-praktikum/api-final-yatube.git
cd api-final-yatube

Cоздать и активировать виртуальное окружение:
python -m venv env
source venv/Scripts/activate

Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:
python manage.py migrate

Запустить проект:
python manage.py runserver

## Примеры запросов к API
Получение JWT-токена
POST http://127.0.0.1:8000/v1/jwt/create/
Body: {"username": "your_username", "password": "your_password"}

Создание поста
POST http://127.0.0.1:8000/v1/posts/
Headers: Authorization: Bearer <your_token>
Body: {"text": "Текст поста", "image": "image_file"}