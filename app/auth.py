import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import SessionLocal
from models import User

# Загрузка .env
load_dotenv()

# Конфигурация
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRE_DAYS: int = int(os.getenv("TOKEN_EXPIRE_DAYS", 3))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env!")

# FastAPI OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
    
# Исключение на случай некорректного токена
credentials_exception = HTTPException(
    status_code=401,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)

# Получение подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Генерация JWT токена
def create_token(user: User) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": user.username,
        "id":  user.id,
        "exp": expires_at,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Получение текущего пользователя из токена
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception

# Хеширование пароля
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

# Проверка пароля
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)
