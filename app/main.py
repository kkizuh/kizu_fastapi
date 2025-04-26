from fastapi import FastAPI, HTTPException, Depends
from database import Base, engine
from models import User
from schemas import RegisterRequest, LoginRequest, TokenResponse
from auth import get_db, create_token, hash_password, verify_password
from transactions import router as transactions_router
from sqlalchemy.orm import Session

app = FastAPI(
    title="🏦 KizuFinTech API",
    description="API для учёта личных финансов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(transactions_router, tags=["💸 Транзакции"])
Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=TokenResponse)
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

@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user)
    return TokenResponse(
        id=user.id,
        token=token,
        username=user.username,
        email=user.email,
        name=user.name
    )
