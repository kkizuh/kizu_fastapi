from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth     import get_db, get_current_user
from models   import Category, User, transaction_categories
from schemas  import CategoryOut, CategoryCreate, CategoryUpdate

router = APIRouter(tags=["📚 Категории"], prefix="/categories")

@router.get("", response_model=list[CategoryOut])
def list_categories(order: str = "id",
                    db: Session = Depends(get_db),
                    _=Depends(get_current_user)):
    ordering = {
        "id": Category.id,
        "name": Category.name,
        "type": Category.type
    }.get(order, Category.id)             
    return db.query(Category).order_by(ordering).all()


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    # проверяем, нет ли такой категории по имени
    if db.query(Category).filter_by(name=data.name).first():
        raise HTTPException(409, "Категория с таким именем уже есть")

    cat = Category(name=data.name, type=data.type)
    db.add(cat)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Категория уже существует")
    db.refresh(cat)
    return cat


@router.patch("/{cat_id}", response_model=CategoryOut)
def patch_category(cat_id: int,
                   data: CategoryUpdate,
                   db: Session = Depends(get_db),
                   user: User  = Depends(get_current_user)):

    cat = db.query(Category).get(cat_id)
    if not cat:
        raise HTTPException(404, "Категория не найдена")

    if data.name is not None:
        cat.name = data.name
    if data.type is not None:
        cat.type = data.type.value

    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{cat_id}", status_code=200,
               summary="Удалить категорию")
def delete_category(cat_id: int,
                    db: Session = Depends(get_db),
                    _=Depends(get_current_user)):
    cat = db.query(Category).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404,
                            detail="Категория не найдена")

    name = cat.name
    db.execute(transaction_categories.delete().where(
        transaction_categories.c.category_id == cat_id
    ))
    db.delete(cat)
    db.commit()

    # ← возвращаем JSON-сообщение
    return {"detail": f"Категория «{name}» (id={cat_id}) удалена"}