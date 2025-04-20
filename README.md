# 🏦 KizuFinTech Backend

Простой backend для управления личными финансами: регистрация пользователей, авторизация с JWT, добавление и просмотр транзакций. Построен на FastAPI и PostgreSQL.

---

## 🚀 Стек технологий

- 🐍 Python 3.11
- ⚡ FastAPI
- 📦 SQLAlchemy
- 🐘 PostgreSQL (через Docker)
- 🔐 JWT (JSON Web Token)
- 🧂 Bcrypt (хэширование паролей)

---

## 🐳 Быстрый старт через Docker

1. Склонируй репозиторий и перейди в папку проекта:

```bash
git clone https://github.com/yourname/kizu-fintech-backend.git
cd kizu-fintech-backend
```

Запусти backend и базу PostgreSQL:
  
```bash
docker-compose up --build
```
API будет доступно на:
```
http://localhost:8000
```
Документация:
```bash
http://localhost:8000/docs
```
