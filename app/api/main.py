from fastapi import APIRouter

from app.api.routes import login, address, company, department, position, role, user, employment

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(address.router)
api_router.include_router(company.router)
api_router.include_router(department.router)
api_router.include_router(employment.router)
api_router.include_router(position.router)
api_router.include_router(role.router)
api_router.include_router(user.router)
