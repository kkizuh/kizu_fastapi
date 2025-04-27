from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user, get_db, hash_password, verify_password
from models import User
from schemas import TokenResponse, UserOut, UserUpdate, PasswordUpdate

router = APIRouter(prefix="/me", tags=["👤 Профиль"])

# GET /me
@router.get("", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    """Текущий профиль"""
    return user

# PATCH /me
@router.patch("", response_model=TokenResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    db.commit(); db.refresh(user)
    return user

# PATCH /me/password
@router.patch("/password")
def change_password(
    data: PasswordUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not verify_password(data.old_password, user.password):
        raise HTTPException(400, "Wrong old password")
    user.password = hash_password(data.new_password)
    db.commit()
    return {"detail": "Password changed"}