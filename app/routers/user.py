from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import crud, models
from app.db.database import get_db
from app.schemas import user as user_schemas
from app.core.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=user_schemas.Token)
def register(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    hashed_password = hash_password(user.password)
    new_user = crud.create_user(db, user, hashed_password)
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=user_schemas.Token)
def login(user: user_schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}