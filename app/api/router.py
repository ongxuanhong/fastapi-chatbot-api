from fastapi import APIRouter
from api.endpoints import user, pot

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(pot.router, prefix="/pots", tags=["Pots"])
