from fastapi import APIRouter

from app.api.routes import login, address, company, department, position, role, user, employment, user_address, \
    user_employment, user_manager, user_role, user_schedule, user_workhour, generator

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(address.router)
api_router.include_router(company.router)
api_router.include_router(department.router)
api_router.include_router(employment.router)
api_router.include_router(position.router)
api_router.include_router(role.router)
api_router.include_router(user.router)
api_router.include_router(user_address.router)
api_router.include_router(user_employment.router)
api_router.include_router(user_manager.router)
api_router.include_router(user_role.router)
api_router.include_router(user_schedule.router)
api_router.include_router(user_workhour.router)
api_router.include_router(generator.router)
