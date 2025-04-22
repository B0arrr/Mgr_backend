from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.api.deps import SessionDep
from app.schemas import UserManager, UserManagerCreate, UserManagerUpdate

router = APIRouter(prefix="/user_manager", tags=["user_manager"])


@router.get("/", response_model=List[UserManager])
async def get_user_managers(db: SessionDep) -> Any:
    """
    Get all user managers
    :param db: Database session
    :return: Returns all user managers
    """
    return crud.user_manager.get_all(db)


@router.get("/{id}", response_model=UserManager)
async def get_user_manager(db: SessionDep, id: int) -> Any:
    """
    Get user manager by id
    :param db: Database session
    :param id: ID of user manager
    :return: Returns user manager
    """
    user_manager = crud.user_manager.get(db, id=id)
    if not user_manager:
        raise HTTPException(status_code=404, detail="User manager not found")
    return user_manager


@router.post("/", response_model=UserManager)
async def create_user_manager(db: SessionDep, obj_in: UserManagerCreate) -> Any:
    """
    Create new user manager
    :param db: Database session
    :param obj_in: User manager object to create
    :return: Returns new user manager
    """
    return crud.user_manager.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=UserManager)
async def update_user_manager(db: SessionDep, id: int, obj_in: UserManagerUpdate) -> Any:
    """
    Update user manager by id
    :param db: Database session
    :param id: Id of user manager
    :param obj_in: User manager object to update
    :return: Returns updated user manager
    """
    user_manager = crud.user_manager.get(db, id=id)
    if not user_manager:
        raise HTTPException(status_code=400, detail="User manager does not exists")
    return crud.user_manager.update(db, db_obj=user_manager, obj_in=obj_in)


@router.delete("/{id}", response_model=UserManager)
async def delete_user_manager(db: SessionDep, id: int) -> Any:
    """
    Delete user manager by id
    :param db: Database session
    :param id: Id of user manager
    :return: Returns deleted user manager
    """
    user_manager = crud.user_manager.get(db, id=id)
    if not user_manager:
        raise HTTPException(status_code=400, detail="User manager does not exists")
    response_data = schemas.UserManager.model_validate(user_manager)
    crud.user_manager.remove(db, id=id)
    return response_data
