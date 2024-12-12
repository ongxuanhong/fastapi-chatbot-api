from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud
from app.db.database import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/pot", tags=["pot"])


@router.get("/")
def get_pot(db: Session = Depends(get_db)):
    """Retrieve the current pot amount."""
    amount = crud.get_pot(db)
    return {"pot_amount": amount}


@router.post("/contribute")
def contribute_to_pot(
    contribution: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a user's contribution to the pot."""
    if contribution <= 0:
        raise HTTPException(
            status_code=400, detail="Contribution must be greater than zero"
        )
    current_pot = crud.get_pot(db)
    updated_pot = crud.update_pot(db, current_pot + contribution)
    return {"message": "Contribution added", "new_pot_amount": updated_pot.amount}


@router.post("/reset")
def reset_pot(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Reset the pot to 0 (e.g., after a user wins)."""
    updated_pot = crud.update_pot(db, 0)
    return {"message": "Pot reset", "new_pot_amount": updated_pot.amount}
