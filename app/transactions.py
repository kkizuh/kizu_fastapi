from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func
from sqlalchemy.orm import Session
from auth import get_db, get_current_user
from models import Transaction, Category, User
from schemas import BalanceResponse, TransactionCreate, TransactionUpdate, TransactionOut
from typing import List

router = APIRouter()

@router.post("/transactions", response_model=TransactionOut)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if data.transaction_type not in ("income", "expense"):
        raise HTTPException(400, "transaction_type must be 'income' or 'expense'")
    new_trx = Transaction(
        title=data.title,
        amount=data.amount,
        type=data.transaction_type,
        date=data.date,
        user_id=user.id
    )
    cats = db.query(Category).filter(Category.id.in_(data.category_ids)).all()
    new_trx.categories = cats

    db.add(new_trx)
    db.commit()
    db.refresh(new_trx)
    return {
        "id":       new_trx.id,
        "title":    new_trx.title,
        "amount":   new_trx.amount,
        "type":     new_trx.type,
        "date":     new_trx.date,
        "categories": [c.id for c in new_trx.categories]
    }

@router.get("/transactions", response_model=List[TransactionOut])
def list_transactions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()

    return [
        {
            "id": trx.id,
            "title": trx.title,
            "amount": trx.amount,
            "transaction_type": trx.type,
            "date": trx.date,
            "categories": [c.id for c in trx.categories],
        }
        for trx in transactions
    ]

@router.patch("/transactions/{trx_id}", response_model=TransactionOut)
def update_transaction(
    trx_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    trx = db.query(Transaction).filter(
        Transaction.id == trx_id,
        Transaction.user_id == user.id
    ).first()
    if not trx:
        raise HTTPException(404, "Транзакция не найдена")

    # обновляем только присланные поля
    if data.title is not None:
        trx.title = data.title
    if data.amount is not None:
        trx.amount = data.amount
    if data.transaction_type is not None:
        trx.type = data.transaction_type.value
    if data.date is not None:
        trx.date = data.date
    if data.category_ids is not None:
        cats = db.query(Category).filter(Category.id.in_(data.category_ids)).all()
        trx.categories = cats

    db.commit()
    db.refresh(trx)
    return {
    "id":       trx.id,
    "title":    trx.title,
    "amount":   trx.amount,
    "transaction_type": trx.type,
    "date":     trx.date,
    "categories": [c.id for c in trx.categories]  # 💥 вот это обязательно!
    }


@router.delete("/transactions/{trx_id}")
def delete_transaction(
    trx_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    trx = db.query(Transaction).filter(
        Transaction.id == trx_id, Transaction.user_id == user.id
    ).first()
    if not trx:
        raise HTTPException(404, "Транзакция не найдена")
    db.delete(trx)
    db.commit()
    return {"detail": "Удалено"}




@router.get("/balance", response_model=BalanceResponse,
            summary="Текущий баланс (доходы, расходы, итог)")
def get_balance(
    db: Session = Depends(get_db),
    user: User  = Depends(get_current_user)
):
    """
    Считает суммы **доходов**, **расходов** и итоговый баланс
    для текущего пользователя одним SQL-запросом.
    """

    # CASE-выражение: если income → +amount, если expense → -amount
    balance_q = (
        db.query(
            func.sum(
                case(
                    (Transaction.type == "income",  Transaction.amount),
                    (Transaction.type == "expense",-Transaction.amount),
                    else_=0.0,
                )
            ).label("total"),
            func.sum(
                case((Transaction.type == "income", Transaction.amount), else_=0.0)
            ).label("income"),
            func.sum(
                case((Transaction.type == "expense", Transaction.amount), else_=0.0)
            ).label("expense"),
        )
        .filter(Transaction.user_id == user.id)
        .one()
    )

    total, income, expense = balance_q

    return BalanceResponse(
        income  = income  or 0.0,
        expense = expense or 0.0,
        total   = total   or 0.0,
    )
