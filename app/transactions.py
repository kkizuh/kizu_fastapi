from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_db, get_current_user
from models import Transaction, Category, User
from schemas import TransactionCreate, TransactionOut
from typing import List

router = APIRouter()

# ✅ Создать транзакцию
@router.post("/transactions", response_model=TransactionOut)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    new_transaction = Transaction(
    title=data.title,
    amount=data.amount,
    type=data.type_,  # ← ИМЕННО type_ (с подчёркиванием)
    date=data.date,
    user_id=user.id
    )

    categories = db.query(Category).filter(Category.id.in_(data.category_ids)).all()
    new_transaction.categories = categories

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# ✅ Получить все свои транзакции
@router.get("/transactions", response_model=List[TransactionOut])
def get_transactions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    return transactions

# ✅ Удалить транзакцию по ID
@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена или не принадлежит вам")

    db.delete(transaction)
    db.commit()
    return {"message": "Транзакция успешно удалена"}
