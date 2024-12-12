from fastapi import FastAPI
from app.routers import user, currency, pot
from app.db.database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user.router)
app.include_router(currency.router)
app.include_router(pot.router)

