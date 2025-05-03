# 🏦 KizuFinTech Backend (`kizu_fastapi`)

**KizuFinTech** — backend‑сервис для управления личными финансами: регистрация → JWT‑авторизация → категории → транзакции → баланс.

---

## 📦 Возможности

- 🔐 Регистрация и логин (JWT / OAuth2 *password flow*)
- 🏷️ CRUD категорий (доходы / расходы)
- 💸 CRUD транзакций + мгновенный баланс (доходы / расходы / итог)
- 🙋‍♂️ `/me` — профиль, смена e‑mail, имени, пароля
- 📊 PostgreSQL + SQLAlchemy ORM
- 🩺 `/healthz` для проверок инфраструктуры
- 🌐 Swagger UI `/docs` и OpenAPI 3.1 (`/openapi.json`)

---

## 🚀 Стек

| Категория    | Технологии                                 |
| ------------ | ------------------------------------------ |
| Backend      | **FastAPI** + Python 3.11                  |
| ORM / DB     | SQLAlchemy 2 · PostgreSQL 15               |
| Auth         | OAuth2 Password flow + JWT (`python-jose`) |
| Безопасность | bcrypt (хэш паролей)                       |
| Dev / CI     | Docker · docker‑compose                    |

---

## ⚙️ Структура проекта

```
kizu_fastapi/
├── app/
│   ├── main.py           # точка входа + include_router(...)
│   ├── auth.py           # JWT, текущий пользователь
│   ├── database.py       # движок + сессия + Base
│   ├── models.py         # ORM‑модели
│   ├── schemas.py        # Pydantic‑схемы
│   ├── users.py          # /me и смена пароля
│   ├── categories.py     # /categories CRUD
│   └── transactions.py   # /transactions CRUD + баланс
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example          # шаблон переменных
└── README.md             # вы читаете его
```

---

## 📂 Переменные окружения

Создайте `.env` и отредактируйте:

```env
# База
POSTGRES_USER=kizuuser
POSTGRES_PASSWORD=kizupass
DB_HOST=db       
DB_PORT=5432
DB_NAME=kizu

# Auth
SECRET_KEY=supersecret123
ALGORITHM=HS256
TOKEN_EXPIRE_DAYS=3
```

> **Не коммитьте** `.env` в репозиторий !

---

## 🐳 Запуск в Docker

```bash
git clone https://github.com/kkizuh/kizu_fastapi.git
cd kizu_fastapi
cp .env.example .env      # правим по‑своему

docker compose up --build
```

- API — [http://localhost:8000](http://localhost:8000)
- Swagger — [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Основные эндпоинты

### Авторизация

| Метод | URL         | Описание                 |
| ----- | ----------- | ------------------------ |
| POST  | `/register` | регистрация пользователя |
| POST  | `/login`    | получить JWT + данные    |

### Профиль (`/me`)

| Метод | URL            | Описание              |
| ----- | -------------- | --------------------- |
| GET   | `/me`          | текущий профиль       |
| PATCH | `/me`          | изменить e‑mail / имя |
| PATCH | `/me/password` | сменить пароль        |

### Категории 📚

| Метод  | URL                      | Описание                              |
| ------ | ------------------------ | ------------------------------------- |
| GET    | `/categories?order=name` | список (order = `id`\|`name`\|`type`) |
| POST   | `/categories`            | создать категорию                     |
| PATCH  | `/categories/{id}`       | частичное изменение                   |
| DELETE | `/categories/{id}`       | удалить категорию                     |

### Транзакции 💸

| Метод  | URL                  | Описание                       |
| ------ | -------------------- | ------------------------------ |
| GET    | `/transactions`      | мои транзакции                 |
| POST   | `/transactions`      | создать                        |
| PATCH  | `/transactions/{id}` | частичное изменение            |
| DELETE | `/transactions/{id}` | удалить                        |
| GET    | `/balance`           | **итог: доходы / расходы / ∑** |

### Health‑check

| Метод | URL        | Описание   |
| ----- | ---------- | ---------- |
| GET   | `/healthz` | всегда 200 |

> Для всех запросов (кроме `/register`, `/login`, `/healthz`) нужен заголовок\
> `Authorization: Bearer <токен>`.

---

## 🧑‍💻 Примеры curl

```bash
# логин
curl -X POST http://localhost:8000/login \
     -H "Content-Type: application/json" \
     -d '{"username":"ivan123","password":"secret123"}'

# авторизация в переменную
TOKEN=$(jq -r .token <<< "$( …команда_выше… )")

# создать категорию
curl -X POST http://localhost:8000/categories \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"name":"Еда","type":"expense"}'

# баланс
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/balance
```

---

## ✅ Завершение работы

```bash
# остановить и удалить контейнеры
docker compose down

# только остановить
docker compose stop
```

---

## 📜 Лицензия

Проект распространяется по [Apache License 2.0](LICENSE).
