from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    id: int
    token: str
    username: str
    email: str
    name: str

class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    category: str
    date: str
