from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import EmploymentCreate, EmploymentUpdate, User, Employment

router = APIRouter(prefix="/employment", tags=["employment"])


@router.get("/", response_model=List[Employment])
async def get_employments(db: SessionDep) -> Any:
    """
    Get all employments
    :param db: Database session
    :return: Returns all employments
    """
    return crud.employment.get_all(db)


@router.get("/{id}", response_model=Employment)
async def get_employment(db: SessionDep, id: int) -> Any:
    """
    Get employment by id
    :param db: Database session
    :param id: Id of the employment
    :return: Returns the employment
    """
    employment = crud.employment.get(db, id=id)
    if not employment:
        raise HTTPException(status_code=404, detail="Employment not found")
    return employment


@router.get("/{id}/users", response_model=List[User])
async def get_employment_users(db: SessionDep, id: int) -> Any:
    """
    Get all employment users
    :param db: Database session
    :param id: Id of the employment
    :return: Returns all employment users
    """
    employment = crud.employment.get(db, id=id)
    if not employment:
        raise HTTPException(status_code=404, detail="Employment not found")
    return employment.users


@router.post("/", response_model=Employment)
async def create_employment(db: SessionDep, obj_in: EmploymentCreate) -> Any:
    """
    Create a new employment
    :param db: Database session
    :param obj_in: Employment object to create
    :return: Returns the employment
    """
    employment = crud.employment.get_by_name(db, name=obj_in.name)
    if employment:
        raise HTTPException(status_code=400, detail="Employment already exists")
    return crud.employment.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=Employment)
async def update_employment(db: SessionDep, id: int, obj_in: EmploymentUpdate) -> Any:
    """
    Update employment by id
    :param db: Database session
    :param id: Id of the employment
    :param obj_in: Employment object to update
    :return: Returns the employment
    """
    employment = crud.employment.get(db, id=id)
    if not employment:
        raise HTTPException(status_code=400, detail="Employment does not exists")
    return crud.employment.update(db, db_obj=employment, obj_in=obj_in)


@router.delete("/{id}", response_model=Employment)
async def delete_employment(db: SessionDep, id: int) -> Any:
    """
    Delete employment by id
    :param db: Database session
    :param id: Id of the employment
    :return: Returns the employment
    """
    employment = crud.employment.get(db, id=id)
    if not employment:
        raise HTTPException(status_code=400, detail="Employment does not exists")
    return crud.employment.remove(db, id=id)
