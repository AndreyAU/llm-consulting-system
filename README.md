# LLM Consulting System

## 📌 Описание проекта

Проект представляет собой двухсервисную систему для работы с LLM (Large Language Model):

- Auth Service — регистрация, логин, JWT
- Bot Service — (будет реализован далее) работа с пользователем и LLM

Сервисы независимы:
- Auth Service не связан с ботом
- Bot Service не хранит пользователей
- Взаимодействие только через JWT

---

## 🏗 Архитектура

### Auth Service
- Регистрация пользователя
- Хеширование пароля (bcrypt)
- Логин и выдача JWT
- Проверка токена
- Endpoint /auth/me

### Bot Service (в разработке)
- Принимает JWT
- Проверяет токен
- Работает с LLM
- Не хранит пользователей

---

## ⚙️ Технологии

- Python 3.12
- FastAPI
- SQLAlchemy (async)
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)
- Pytest
- HTTPX

---
## 🚀 Запуск проекта

1. Клонировать репозиторий

git clone https://github.com/AndreyAU/llm-consulting-system.git

2. Перейти в папку сервиса

cd llm-consulting-system/auth_service

3. Установить зависимости

uv sync

4. Запустить сервер

uv run uvicorn app.main:app --reload

5. Открыть Swagger

http://127.0.0.1:8000/docs

---

## 🔐 API Auth Service

POST /auth/register — регистрация  
POST /auth/login — получение JWT  
GET /auth/me — данные пользователя по токену  

---

## 🧪 Тестирование

### Модульные тесты

Файл: tests/test_security.py

Проверяют:
- hash_password
- verify_password
- create_access_token
- decode_token
- наличие полей sub, role, iat, exp

---

### Интеграционные тесты

Файл: tests/test_auth_api.py

Проверяется полный сценарий:

1. POST /auth/register
2. POST /auth/login
3. GET /auth/me (с токеном)

Используется:
- in-memory SQLite
- httpx ASGITransport
- override зависимостей

---

### Негативные тесты

Проверяются:

- повторная регистрация → 409
- неверный пароль → 401
- нет токена → 401
- неверный токен → 401

---

## 📸 Скриншоты

### Swagger UI
![Swagger](docs/images/swagger_main.png)

### Регистрация
![Register](docs/images/auth_register_success.png)

### Логин
![Login](docs/images/auth_login_success.png)

### /auth/me
![Me](docs/images/auth_me_success.png)

### Тесты
![Tests](docs/images/auth_tests_passed.png)

---

## 🔑 Сценарий работы

1. Пользователь регистрируется
2. Логинится
3. Получает JWT
4. Использует токен для /auth/me
5. Передаёт токен в Bot Service

---

## 📌 Пример пользователя

andreenko@email.com

---

## 📊 Соответствие требованиям

✔ Разделение сервисов  
✔ JWT только в Auth Service  
✔ Пароли хешируются  
✔ /auth/me защищён  
✔ Тесты реализованы  
✔ Swagger работает  

---

## 📎 Примечания

JWT содержит:
- sub
- role
- iat
- exp

Пароли не хранятся в открытом виде

---

## 👨‍💻 Автор

Andreenko
