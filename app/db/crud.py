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
