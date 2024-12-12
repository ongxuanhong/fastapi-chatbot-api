from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user as user_schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: user_schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_balance(db: Session, user_id: int) -> int:
    """Retrieve the user's current balance."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user.balance if user else None


def update_user_balance(db: Session, user_id: int, amount: int):
    """Update the user's balance by adding or deducting an amount."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.balance += amount
        db.commit()
        db.refresh(user)
        return user
    return None


def get_pot(db: Session) -> int:
    """Retrieve the current pot amount."""
    pot = db.query(models.Pot).first()
    if not pot:
        pot = models.Pot(amount=0)
        db.add(pot)
        db.commit()
        db.refresh(pot)
    return pot.amount


def update_pot(db: Session, amount: int):
    """Add to the pot or reset it."""
    pot = db.query(models.Pot).first()
    if not pot:
        pot = models.Pot(amount=amount)
        db.add(pot)
    else:
        pot.amount = amount
    db.commit()
    db.refresh(pot)
    return pot


def increment_message_count(db: Session, user_id: int):
    """Increment the message count for a user."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.message_count += 1
        db.commit()
        db.refresh(user)
        return user.message_count
    return None


def calculate_message_cost(message_count: int) -> int:
    """Calculate the cost of the next message based on the user's message count."""
    return 5 * message_count  # Example: Cost increases by 5 units per message
