from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import Position, User, PositionCreate, PositionUpdate

router = APIRouter(prefix="/position", tags=["position"])


@router.get("/", response_model=List[Position])
async def get_positions(db: SessionDep) -> Any:
    """
    Get all positions
    :param db: Database session
    :return: Returns all positions
    """
    return crud.position.get_all(db)


@router.get("/{id}", response_model=Position)
async def get_position(db: SessionDep, id: int) -> Any:
    """
    Get position by id
    :param db: Database session
    :param id: ID of the position
    :return: Returns the position
    """
    position = crud.position.get(db, id=id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.get("/{id}/users", response_model=List[User])
async def get_users_from_position(db: SessionDep, id: int) -> Any:
    """
    Get all users from position
    :param db: Database session
    :param id: Id of the position
    :return: Returns all users
    """
    position = crud.position.get(db, id=id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position.users


@router.post("/", response_model=Position)
async def create_position(db: SessionDep, obj_in: PositionCreate) -> Any:
    """
    Create a new position
    :param db: Database session
    :param obj_in: Position object to create
    :return: Returns the new position
    """
    position = crud.position.get_by_name(db, name=obj_in.name)
    if position:
        raise HTTPException(status_code=400, detail="Position already exists")
    return crud.position.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=Position)
async def update_position(db: SessionDep, id: int, obj_in: PositionUpdate) -> Any:
    """
    Update a position
    :param db: Database session
    :param id: Id of the position
    :param obj_in: Position object to update
    :return: Returns the updated position
    """
    position = crud.position.get(db, id=id)
    if not position:
        raise HTTPException(status_code=400, detail="Position does not exists")
    return crud.position.update(db, db_obj=position, obj_in=obj_in)


@router.delete("/{id}", response_model=Position)
async def delete_position(db: SessionDep, id: int) -> Any:
    """
    Delete a position
    :param db: Database session
    :param id: Id of the position
    :return: Returns the deleted position
    """
    position = crud.position.get(db, id=id)
    if not position:
        raise HTTPException(status_code=400, detail="Position does not exists")
    return crud.position.remove(db, id=id)
