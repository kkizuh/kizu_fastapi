from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# 📦 Регистрация
class RegisterRequest(BaseModel):
    username: str = Field(..., example="ivan123", description="Имя пользователя (логин)")
    email: str = Field(..., example="ivan@example.com", description="Электронная почта")
    name: str = Field(..., example="Иван Иванов", description="Отображаемое имя пользователя")
    password: str = Field(..., example="supersecure123", description="Пароль (не менее 6 символов)")

# 🔐 Вход
class LoginRequest(BaseModel):
    username: str = Field(..., example="ivan123", description="Имя пользователя")
    password: str = Field(..., example="supersecure123", description="Пароль")

# 🔐 Ответ при авторизации
class TokenResponse(BaseModel):
    id: int = Field(..., example=1, description="ID пользователя")
    token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", description="JWT-токен")
    username: str = Field(..., example="ivan123")
    email: str = Field(..., example="ivan@example.com")
    name: str = Field(..., example="Иван Иванов")

# 🧾 Категория
class CategoryOut(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True

# 💰 Создание транзакции
class TransactionCreate(BaseModel):
    title: str = Field(..., example="Покупка кофе")
    amount: float = Field(..., example=250.0)
    transaction_type: Literal["income", "expense"] = Field(..., alias="type", description="Тип транзакции")
    category: str = Field(..., example="еда")
    date: date = Field(..., example="2025-04-20")

    class Config:
        populate_by_name = True

# 💰 Просмотр транзакции
class TransactionOut(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    date: date
    categories: List[CategoryOut]

    class Config:
        orm_mode = True
