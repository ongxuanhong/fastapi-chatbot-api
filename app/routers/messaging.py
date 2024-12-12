import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud
from app.db.database import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/messages", tags=["messaging"])


@router.post("/send")
def send_message(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send a message, deduct currency, and check if the user wins the pot."""
    user_id = current_user["id"]

    # Get current message count and calculate cost
    message_count = crud.increment_message_count(db, user_id)
    if message_count is None:
        raise HTTPException(status_code=404, detail="User not found")

    message_cost = crud.calculate_message_cost(message_count)

    # Check if the user has enough balance
    user_balance = crud.get_user_balance(db, user_id)
    if user_balance < message_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Deduct message cost
    crud.update_user_balance(db, user_id, -message_cost)

    # Add message cost to the pot
    current_pot = crud.get_pot(db)
    updated_pot = crud.update_pot(db, current_pot + message_cost)

    # Randomized logic to determine if the user wins
    win_chance = random.random()  # Generate a number between 0 and 1
    if win_chance < 0.1:  # Example: 10% chance to win
        # User wins the pot
        crud.update_user_balance(db, user_id, updated_pot.amount)
        crud.update_pot(db, 0)  # Reset the pot
        return {
            "message": "Congratulations! You won the pot!",
            "pot_amount": updated_pot.amount,
        }

    return {
        "message": "Sorry, better luck next time!",
        "pot_amount": updated_pot.amount,
    }
