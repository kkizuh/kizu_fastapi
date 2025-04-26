from enum import Enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict 


class TransactionType(str, Enum):
    INCOME  = "income"
    EXPENSE = "expense"


# ------------ auth -------------
class RegisterRequest(BaseModel):
    username: str = Field(..., example="ivan123", description="Логин")
    email:    str = Field(..., example="ivan@example.com", description="E-mail")
    name:     str = Field(..., example="Иван Иванов", description="Имя")
    password: str = Field(..., min_length=6, example="secret123", description="Пароль")


class LoginRequest(BaseModel):
    username: str = Field(..., example="ivan123")
    password: str = Field(..., example="secret123")

class UserOut(BaseModel):
    id:       int
    username: str
    email:    str
    name:     str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name:  Optional[str]      = None

class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    id:       int
    token:    str
    username: str
    email:    str
    name:     str

    model_config = ConfigDict(from_attributes=True)   # заменяет orm_mode


# ------------ categories -------------
class CategoryOut(BaseModel):
    id:   int
    name: str
    type: TransactionType

    model_config = ConfigDict(from_attributes=True)


# ------------ transactions -------------
class TransactionCreate(BaseModel):
    title:            str             = Field(..., example="Кофе")
    amount:           float           = Field(..., example=150.0)
    transaction_type: TransactionType = Field(..., example=TransactionType.EXPENSE)
    category_ids:     List[int]       = Field(..., example=[1, 2])
    date: datetime = Field(..., example="2025-04-26T15:45:00Z")


class TransactionOut(BaseModel):
    id:   int
    title: str
    amount: float
    transaction_type: TransactionType = Field(alias="type")

    date: datetime
    categories: List[CategoryOut]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class TransactionUpdate(BaseModel):
    """Все поля опциональны — можно прислать только то, что меняем"""
    title:            Optional[str]             = Field(None, example="Обед")
    amount:           Optional[float]           = Field(None, example=300.0)
    transaction_type: Optional[TransactionType] = Field(None, example=TransactionType.INCOME)
    category_ids:     Optional[List[int]]       = Field(None, example=[3])
    date:             Optional[datetime]        = Field(None, example="2025-04-26T15:12:00")

class BalanceResponse(BaseModel):
    income:  float
    expense: float
    total:   float