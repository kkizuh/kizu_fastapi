from fastapi import FastAPI, HTTPException, Depends
from database import Base, engine
from models import User
from schemas import LoginRequest, RegisterRequest, TokenResponse
from auth import get_db, create_token, hash_password, verify_password
from transactions import router as transactions_router
from sqlalchemy.orm import Session
from users import router as user_router
from categories import router as categories_router


app = FastAPI(
    title="🏦 KizuFinTech API",
    description="""
    API-сервис для Android-приложения KizuFinTech.

    📌 Возможности:
    - 🔐 Регистрация и авторизация пользователей
    - 💸 Управление транзакциями: добавление, редактирование, удаление, фильтрация
    - 🗂 Управление категориями доходов и расходов
    - 👤 Работа с профилем пользователя

    ⚠️ API является приватным и предназначен для авторизованных клиентов.
    """,
    version="1.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    license_info={
        "name": "Apache License 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=TokenResponse, tags=["👤 Профиль"])
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=data.username,
        email=data.email,
        name=data.name,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user)
    return TokenResponse(
        id=user.id,
        token=token,
        username=user.username,
        email=user.email,
        name=user.name
    )

@app.post("/login", response_model=TokenResponse, tags=["👤 Профиль"])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Принимает **application/json**:
    {
      "username": "ivan123",
      "password": "secret1234"
    }
    Возвращает JWT-токен и сведения о пользователе.
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(user)
    return TokenResponse(
        id=user.id,
        token=token,
        username=user.username,
        email=user.email,
        name=user.name,
    )

app.include_router(user_router, prefix="/users", tags=["👤 Профиль"])
app.include_router(transactions_router, tags=["💸 Транзакции"])
app.include_router(categories_router, tags=["📚 Категории"])
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
