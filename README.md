# LLM Consulting System

## 📌 Описание проекта

Проект представляет собой двухсервисную систему для работы с LLM (Large Language Model) с использованием JWT-аутентификации и асинхронной обработки запросов.

Система состоит из:

- Auth Service — регистрация пользователей, логин и выпуск JWT
- Bot Service — Telegram-бот, принимающий запросы пользователей и отправляющий их в LLM через очередь

Сервисы полностью изолированы и взаимодействуют только через JWT.

---

## 🏗 Архитектура системы

### Auth Service
- Регистрация пользователя
- Хеширование пароля (bcrypt)
- Логин и выдача JWT
- Проверка токена
- Endpoint /auth/me

### Bot Service
- Принимает JWT от пользователя
- Валидирует токен (подпись + срок)
- Сохраняет токен в Redis
- Принимает сообщения из Telegram
- Публикует задачи в RabbitMQ
- Не выполняет запрос к LLM напрямую

### Асинхронная обработка
- Bot Service → отправляет задачу
- RabbitMQ → очередь сообщений
- Celery Worker → обрабатывает задачу
- OpenRouter API → получает ответ LLM

---

## ⚙️ Технологии

- Python 3.12
- FastAPI
- SQLAlchemy (async)
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)
- Aiogram
- Redis
- RabbitMQ
- Celery
- HTTPX
- Pytest
- Fakeredis
- Pytest-mock
- Respx

---

## 🚀 Запуск проекта

git clone https://github.com/AndreyAU/llm-consulting-system.git  
cd llm-consulting-system  
docker compose up --build  

---

## 🔐 API Auth Service

- POST /auth/register — регистрация  
- POST /auth/login — получение JWT  
- GET /auth/me — данные пользователя по токену  

Swagger:  
http://127.0.0.1:8000/docs  

---

## 🤖 Сценарий работы Telegram-бота

1. Пользователь запускает бота (/start)  
2. Отправляет JWT: /token <JWT>  
3. Бот сохраняет токен в Redis  
4. Пользователь отправляет запрос  
5. Бот валидирует JWT  
6. Бот отправляет задачу в RabbitMQ  
7. Celery Worker обрабатывает задачу  
8. Ответ возвращается пользователю  

---

## 🧪 Тестирование

### Auth Service

Модульные тесты:
- hash_password
- verify_password
- create_access_token
- decode_token

Интеграционные тесты:
- регистрация
- логин
- /auth/me

Негативные тесты:
- повторная регистрация → 409
- неверный пароль → 401
- нет токена → 401
- неверный токен → 401

---

### Bot Service

Модульные тесты:
- проверка JWT
- обработка ошибок

Мок-тесты:
- fakeredis
- pytest-mock

Проверяется:
- сохранение токена
- отказ без токена
- вызов Celery

Интеграционные тесты:
- respx
- проверка OpenRouter

---
## 📸 Скриншоты

### Swagger Auth Service
![Swagger](docs/images/swagger_main.png)

### Регистрация
![Register](docs/images/auth_register_success.png)

### Логин
![Login](docs/images/auth_login_success.png)

### /auth/me
![Me](docs/images/auth_me_success.png)

### Тесты Auth
![Auth Tests](docs/images/auth_tests_passed.png)

---

### Telegram Bot (workflow)
![Telegram](docs/images/telegram_bot_workflow.png)

---

### RabbitMQ (очереди и активность)
![RabbitMQ](docs/images/rabbitmq_activity_example.png)

---

### Тесты Bot Service (общие)
![Bot Tests](docs/images/bot_tests_success.png)

---

### Тесты обработчиков (handlers)
![Handlers Tests](docs/images/bot_handlers_tests_success.png)

---

### Полный прогон тестов Bot Service
![All Bot Tests](docs/images/bot_all_tests_success.png)

---

## 🔑 Пример пользователя

andreenko@email.com

---

## 📊 Соответствие требованиям

✔ Разделение на два сервиса  
✔ JWT создаётся только в Auth Service  
✔ Bot Service валидирует токен  
✔ Redis используется  
✔ RabbitMQ используется  
✔ Celery используется  
✔ Асинхронная обработка реализована  
✔ Тесты реализованы и проходят  
✔ Все сценарии подтверждены скриншотами  

---

## 📎 Примечания

JWT содержит:
- sub
- role
- iat
- exp

Пароли хешируются и не хранятся в открытом виде.

---

## 👨‍💻 Автор

Andreenko
