# 🏦 KizuFinTech Backend

**KizuFinTech** — это backend-сервис для управления личными финансами.  
Система поддерживает регистрацию, JWT-авторизацию, создание и удаление транзакций, просмотр пользователей (включая админ-функции).

---

## 📦 Возможности

- 🔐 Регистрация и авторизация по логину/паролю
- 🧾 Хранение JWT-токена
- 💰 Добавление, просмотр и удаление транзакций
- 🧑 Просмотр всех пользователей (админ)
- 📊 Сохранение транзакций в PostgreSQL
- ⚙️ Готов для подключения Android-клиента через API

---

## 🚀 Стек технологий

| Категория         | Технологии                   |
|------------------|------------------------------|
| Backend          | FastAPI, Python 3.11         |
| ORM              | SQLAlchemy                   |
| База данных      | PostgreSQL (в Docker)        |
| Авторизация      | JWT (OAuth2PasswordBearer)   |
| Безопасность     | Bcrypt (хэширование паролей) |
| Тестирование     | pytest, httpx *(опционально)*|
| Docker           | docker-compose               |

---

## ⚙️ Архитектура проекта

```
kizu_fastapi/
├── app/
│   ├── main.py              # Точка входа
│   ├── auth.py              # JWT логика
│   ├── database.py          # SQLAlchemy + PostgreSQL
│   ├── models.py            # ORM-модели
│   ├── schemas.py           # Pydantic-схемы
│   ├── transactions.py      # Роуты транзакций
│   └── tests/               # Юнит-тесты
├── .env                     # Секреты (не коммитить)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📂 Переменные окружения (.env)

Создай файл `.env` в корне:

```env
POSTGRES_DB=kizu
POSTGRES_USER=kizuuser
POSTGRES_PASSWORD=kizupass
DB_HOST=db
DB_PORT=5432
DB_NAME=kizu
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

> ⚠️ Добавь `.env` в `.gitignore`, чтобы не сливать секреты в Git

---

## 🐳 Быстрый старт с Docker

### 1. Склонируй репозиторий:

```bash
git clone https://github.com/yourname/kizu-fintech-backend.git
cd kizu-fintech-backend
```

### 2. Создай `.env` и запусти backend + PostgreSQL:

```bash
docker-compose up --build
```

### 3. Проверка работы API:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

---

## 📚 Эндпоинты API (Swagger)

### 🔐 Авторизация

| Метод | URL         | Описание        |
|-------|-------------|-----------------|
| POST  | `/register` | Регистрация     |
| POST  | `/login`    | Получить токен  |

### 💸 Транзакции *(нужен JWT)*

| Метод  | URL                    | Описание                   |
|--------|------------------------|----------------------------|
| GET    | `/transactions`        | Список своих транзакций    |
| POST   | `/transactions`        | Добавить транзакцию        |
| DELETE | `/transactions/{id}`   | Удалить транзакцию по ID   |

### 🧑 Админ-функции

| Метод | URL                                 | Описание                      |
|-------|--------------------------------------|-------------------------------|
| GET   | `/admin/users`                      | Получить всех пользователей   |
| GET   | `/admin/users/{user_id}/transactions` | Получить транзакции юзера     |

---

## 📥 Пример запроса в Swagger (/docs)

### 🔐 Авторизация и JWT

1. Отправь `POST /login` с JSON:

```json
{
  "username": "testuser",
  "password": "123456"
}
```

2. Скопируй токен из ответа

3. Нажми "Authorize" в Swagger UI → вставь:

```
Bearer <твой_токен>
```

Теперь все запросы будут авторизованы.

---

## 🧪 (опционально) Локальный запуск без Docker

1. Установи Python и зависимости:

```bash
pip install -r requirements.txt
```

2. Запусти PostgreSQL локально (или через PgAdmin)

3. Настрой `.env`, подключись к БД

4. Запусти сервер:

```bash
uvicorn app.main:app --reload
```

---

## ✅ Завершение сервера

- `Ctrl + C` — для локального
- `docker-compose down` — для Docker
- `docker-compose stop` — остановить, но не удалить

---

## 🔒 Рекомендации по безопасности

- Используй `.env.example` вместо настоящего `.env` в Git
- Никогда не пушь `SECRET_KEY` в открытый репозиторий
- Добавь `is_admin` для защиты админ-функций
- Добавь HTTPS, если разворачиваешь в прод

---

## 📜 Лицензия

Проект создан для обучения, дипломной работы и pet-практики.  
MIT — можно использовать и дорабатывать свободно.
