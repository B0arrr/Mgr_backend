from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import UserAddress, UserAddressCreate, UserAddressUpdate

router = APIRouter(prefix="/user_address", tags=["user_address"])


@router.get("/", response_model=List[UserAddress])
async def get_user_addresses(db: SessionDep) -> Any:
    """
    Get all user addresses
    :param db: Database session
    :return: Returns all user addresses
    """
    return crud.user_address.get_all(db)


@router.get("/{id}", response_model=UserAddress)
async def get_user_address(db: SessionDep, id: int) -> Any:
    """
    Get user address by id
    :param db: Database session
    :param id: ID of the user address
    :return: Returns user address
    """
    user_address = crud.user_address.get(db, id=id)
    if not user_address:
        raise HTTPException(status_code=404, detail="User address not found")
    return user_address


@router.post("/", response_model=UserAddress)
async def create_user_address(db: SessionDep, obj_in: UserAddressCreate) -> Any:
    """
    Create new user address
    :param db: Database session
    :param obj_in: User address object to create
    :return: Returns new user address
    """
    return crud.user_address.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=UserAddress)
async def update_user_address(db: SessionDep, id: int, obj_in: UserAddressUpdate) -> Any:
    """
    Update user address by id
    :param db: Database session
    :param id: ID of the user address
    :param obj_in: User address object to update
    :return: Returns updated user address
    """
    user_address = crud.user_address.get(db, id=id)
    if not user_address:
        raise HTTPException(status_code=400, detail="User address does not exists")
    return crud.user_address.update(db, db_obj=user_address, obj_in=obj_in)


@router.delete("/{id}", response_model=UserAddress)
async def delete_user_address(db: SessionDep, id: int) -> Any:
    """
    Delete user address by id
    :param db: Database session
    :param id: Id of the user address
    :return: Returns deleted user address
    """
    user_address = crud.user_address.get(db, id=id)
    if not user_address:
        raise HTTPException(status_code=400, detail="User address does not exists")
    return crud.user_address.remove(db, id=id)
