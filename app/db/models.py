from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Integer, default=100)


class Pot(Base):
    __tablename__ = "pot"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=0)  # Default pot amount is 0
