from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import crud
from app.db.database import get_db
from app.schemas.user import UserBalance
from app.core.auth import get_current_user

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/balance", response_model=UserBalance)
def get_balance(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Fetch the current balance of the logged-in user."""
    user_balance = crud.get_user_balance(db, current_user["id"])
    if user_balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"balance": user_balance}


@router.post("/deduct")
def deduct_balance(
    cost: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Deduct a specific amount of currency from the user's balance."""
    user_balance = crud.get_user_balance(db, current_user["id"])
    if user_balance is None or user_balance < cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance"
        )

    updated_user = crud.update_user_balance(db, current_user["id"], -cost)
    return {"message": "Currency deducted", "new_balance": updated_user.balance}
