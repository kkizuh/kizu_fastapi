from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
from models import Transaction
from schemas import TransactionCreate
from typing import List
from models import Transaction, User

router = APIRouter()

# ✅ Добавить транзакцию
@router.post("/transactions")
def add_transaction(data: TransactionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_trx = Transaction(user_id=user.id, **data.dict())
    db.add(db_trx)
    db.commit()
    return {"message": "Transaction added"}



# ✅ Получить свои транзакции
@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db), user=Depends(get_current_user)):
    trx = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "amount": t.amount,
            "type": t.type,
            "category": t.category,
            "date": t.date
        }
        for t in trx
    ]



# ✅ Удалить свою транзакцию по ID
@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    trx = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
    if not trx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(trx)
    db.commit()
    return {"message": "Transaction deleted"}


# 🔍 Админ: получить всех пользователей
@router.get("/admin/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "name": u.name
        } for u in users
    ]


# 🔍 Админ: получить все транзакции пользователя по его ID
@router.get("/admin/users/{user_id}/transactions")
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    trx = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "amount": t.amount,
            "type": t.type,
            "category": t.category,
            "date": t.date
        } for t in trx
    ]