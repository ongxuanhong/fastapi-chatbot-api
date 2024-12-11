import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your CockroachDB connection string
DATABASE_URL = os.environ["DATABASE_URL"]
print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()