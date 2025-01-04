from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import Address, AddressCreate, AddressUpdate, User

router = APIRouter(prefix="/address", tags=["address"])


@router.get("/", response_model=List[Address])
async def get_addresses(db: SessionDep) -> Any:
    """
    Get all addresses
    :param db: Database session
    :return: Returns list of addresses
    """
    return crud.address.get_all(db=db)


@router.get("/{id}", response_model=Address)
async def get_address(db: SessionDep, id: int) -> Any:
    """
    Get a specific address
    :param db: Database session
    :param id: Id of address to get
    :return: Returns address
    """
    address = crud.address.get(db=db, id=id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.get("/{id}/users", response_model=List[User])
async def get_users_from_address(db: SessionDep, id: int) -> Any:
    """
    Get users from address
    :param db: Database session
    :param id: Id of user
    :return: Returns list of users
    """
    address = crud.address.get(db=db, id=id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address.users


@router.post("/", response_model=Address)
async def create_address(db: SessionDep, obj_in: AddressCreate) -> Any:
    """
    Create a new address
    :param db: Database session
    :param obj_in: Address object to create
    :return: Returns new created address
    """
    address = crud.address.get_by_street_and_city(db=db, city=obj_in.city, street=obj_in.street)
    if address:
        raise HTTPException(status_code=400, detail="Address already exists")
    return crud.address.create(db=db, obj_in=obj_in)


@router.put("/{id}", response_model=Address)
async def update_address(db: SessionDep, id: int, obj_in: AddressUpdate) -> Any:
    """
    Update an existing address
    :param db: Database session
    :param id: Id of address to update
    :param obj_in: Address object to update
    :return: Returns updated address
    """
    address = crud.address.get(db=db, id=id)
    if not address:
        raise HTTPException(status_code=400, detail="Address does not exist")
    return crud.address.update(db=db, db_obj=address, obj_in=obj_in)


@router.delete("/{id}", response_model=Address)
async def delete_address(db: SessionDep, id: int) -> Any:
    """
    Delete an existing address
    :param db: Database session
    :param id: Id of address to delete
    :return: Returns deleted address
    """
    address = crud.address.get(db=db, id=id)
    if not address:
        raise HTTPException(status_code=400, detail="Address does not exist")
    return crud.address.remove(db=db, id=id)
