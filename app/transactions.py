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
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_transaction = Transaction(
        title=data.title,
        amount=data.amount,
        type=data.type,
        date=data.date,
        user_id=user.id
    )

    categories = db.query(Category).filter(Category.id.in_(data.category_ids)).all()
    new_transaction.categories = categories

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction



# ✅ Получить свои транзакции
@router.post("/transactions")
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_transaction = Transaction(
        title=data.title,
        amount=data.amount,
        type=data.type,
        date=data.date,
        user_id=user.id
    )

    categories = db.query(Category).filter(Category.id.in_(data.category_ids)).all()
    new_transaction.categories = categories

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction



# ✅ Удалить свою транзакцию по ID
@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена или не принадлежит вам")

    db.delete(transaction)
    db.commit()
    return {"message": "Транзакция успешно удалена"}


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