from fastapi import APIRouter

from app.api.routes import login, address

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(address.router)
