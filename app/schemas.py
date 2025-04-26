from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import date

# 📦 Регистрация
class RegisterRequest(BaseModel):
    username: str = Field(..., example="ivan123", description="Имя пользователя (логин)")
    email:    str = Field(..., example="ivan@example.com", description="Электронная почта")
    name:     str = Field(..., example="Иван Иванов", description="Отображаемое имя")
    password: str = Field(..., example="supersecure123", description="Пароль (не менее 6 символов)")

# 🔐 Вход
class LoginRequest(BaseModel):
    username: str = Field(..., example="ivan123", description="Имя пользователя")
    password: str = Field(..., example="supersecure123", description="Пароль")

# 🔐 Ответ при авторизации
class TokenResponse(BaseModel):
    id:       int
    token:    str
    username: str
    email:    str
    name:     str

    class Config:
        from_attributes = True

# 📚 Категория (вывод)
class CategoryOut(BaseModel):
    id:   int
    name: str
    type: Literal["income", "expense"]

    class Config:
        from_attributes = True

# 💸 Создание транзакции
class TransactionCreate(BaseModel):
    title:   str                 = Field(..., example="Покупка кофе")
    amount:  float               = Field(..., example=250.0)
    type_:   Literal["income", "expense"] = Field(..., alias="type", description="income или expense")
    category_ids: List[int]      = Field(..., example=[1,2], description="Список ID категорий")
    date:    date                = Field(..., example="2025-04-20")

    class Config:
        from_attributes    = True   # вместо orm_mode
        populate_by_name   = True   # чтобы Pydantic понимал alias="type"

# 💸 Вывод транзакции
class TransactionOut(BaseModel):
    id:        int
    title:     str
    amount:    float
    type_:     Literal["income", "expense"] = Field(..., alias="type")
    date:      date
    categories: List[CategoryOut]

    class Config:
        from_attributes    = True
        populate_by_name   = True