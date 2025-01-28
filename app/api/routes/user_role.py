from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import UserRole, UserRoleCreate, UserRoleUpdate

router = APIRouter(prefix="/user_role", tags=["user_role"])


@router.get("/", response_model=List[UserRole])
async def get_user_roles(db: SessionDep) -> Any:
    """
    Get all user roles
    :param db: DB session
    :return: Returns all user roles
    """
    return crud.user_role.get_all(db)


@router.get("/{id}", response_model=UserRole)
async def get_user_role(db: SessionDep, id: int) -> Any:
    """
    Get user role by id
    :param db: DB session
    :param id: Id of the user role
    :return: Returns user role
    """
    user_role = crud.user_role.get(db, id=id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return user_role


@router.post("/", response_model=UserRole)
async def create_user_role(db: SessionDep, obj_in: UserRoleCreate) -> Any:
    """
    Create new user role
    :param db: DB session
    :param obj_in: User role object to create
    :return: Returns new user role
    """
    return crud.user_role.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=UserRole)
async def update_user_role(db: SessionDep, id: int, obj_in: UserRoleUpdate) -> Any:
    """
    Update user role by id
    :param db: Database session
    :param id: Id of the user role
    :param obj_in: User role object to update
    :return: Returns updated user role
    """
    user_role = crud.user_role.get(db, id=id)
    if not user_role:
        raise HTTPException(status_code=400, detail="User role does not exists")
    return crud.user_role.update(db, db_obj=user_role, obj_in=obj_in)


@router.delete("/{id}", response_model=UserRole)
async def delete_user_role(db: SessionDep, id: int) -> Any:
    """
    Delete user role by id
    :param db: Database session
    :param id: Id of the user role
    :return: Returns deleted user role
    """
    user_role = crud.user_role.get(db, id=id)
    if not user_role:
        raise HTTPException(status_code=400, detail="User role does not exists")
    return crud.user_role.remove(db, id=id)
