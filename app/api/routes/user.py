from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.schemas import User, UserCreate, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=List[User])
async def get_all_users(db: SessionDep) -> Any:
    """
    Get all users
    :param db: Database session
    :return: Returns all users
    """
    return crud.user.get_all(db)


@router.get("/{id}", response_model=User)
async def get_user(db: SessionDep, id: int) -> Any:
    """
    Get user by id
    :param db: Database session
    :param id: Id of the user
    :return: Returns user
    """
    user = crud.user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User)
async def create_user(db: SessionDep, obj_in: UserCreate) -> Any:
    """
    Create new user
    :param db: Database session
    :param obj_in: User object to create
    :return: Returns new user
    """
    user = crud.user.get_by_email(db, email=obj_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    obj_in.password = get_password_hash(obj_in.password)
    return crud.user.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=User)
async def update_user(db: SessionDep, id: int, obj_in: UserUpdate) -> Any:
    """
    Update user by id
    :param db: Database session
    :param id: Id of the user
    :param obj_in: User object to update
    :return: Returns updated user
    """
    user = crud.user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exists")
    return crud.user.update(db, db_obj=user, obj_in=obj_in)


@router.delete("/{id}", response_model=User)
async def delete_user(db: SessionDep, id: int) -> Any:
    """
    Delete user by id
    :param db: Database session
    :param id: Id of the user
    :return: Returns deleted user
    """
    user = crud.user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exists")
    return crud.user.update(db, db_obj=user, obj_in={"is_active": False})
