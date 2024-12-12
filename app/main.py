from fastapi import FastAPI
from app.routers import user
from app.db.database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user.router)
