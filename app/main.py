from fastapi import FastAPI
from api.router import api_router
from core.config import settings
from db.session import engine, Base

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

# Include API routers
app.include_router(api_router)
