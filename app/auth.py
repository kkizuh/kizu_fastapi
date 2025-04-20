from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(user: User):
    data = {"sub": user.username, "id": user.id}
    expire = datetime.utcnow() + timedelta(days=3)
    data["exp"] = expire
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str):
    return bcrypt.hash(password)

def verify_password(password: str, hash: str):
    return bcrypt.verify(password, hash)
