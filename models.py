from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    balance = Column(Integer, default=100)  # Default virtual currency
