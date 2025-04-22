from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.api.deps import SessionDep
from app.schemas import UserEmployment, UserEmploymentCreate, UserEmploymentUpdate

router = APIRouter(prefix="/user_employment", tags=["user_employment"])


@router.get("/", response_model=List[UserEmployment])
async def get_user_employments(db: SessionDep) -> Any:
    """
    Get all user employments
    :param db: DB session
    :return: Returns all user employments
    """
    return crud.user_employment.get_all(db)


@router.get("/{id}", response_model=UserEmployment)
async def get_user_employment(db: SessionDep, id: int) -> Any:
    """
    Get user employment by id
    :param db: Database session
    :param id: Id of the user employment
    :return: Returns user employment
    """
    user_employment = crud.user_employment.get(db, id=id)
    if not user_employment:
        raise HTTPException(status_code=404, detail="User employment not found")
    return user_employment


@router.post("/", response_model=UserEmployment)
async def create_user_employment(db: SessionDep, obj_in: UserEmploymentCreate) -> Any:
    """
    Create new user employment
    :param db: Database session
    :param obj_in: User employment object to create
    :return: Returns new user employment
    """
    return crud.user_employment.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=UserEmployment)
async def update_user_employment(db: SessionDep, id: int, obj_in: UserEmploymentUpdate) -> Any:
    """
    Update user employment by id
    :param db: Database session
    :param id: Id of the user employment
    :param obj_in: User employment object to update
    :return: Returns updated user employment
    """
    user_employment = crud.user_employment.get(db, id=id)
    if not user_employment:
        raise HTTPException(status_code=400, detail="User employment does not exists")
    return crud.user_employment.update(db, db_obj=user_employment, obj_in=obj_in)


@router.delete("/{id}", response_model=UserEmployment)
async def delete_user_employment(db: SessionDep, id: int) -> Any:
    """
    Delete user employment by id
    :param db: Database session
    :param id: Id of the user employment
    :return: Returns deleted user employment
    """
    user_employment = crud.user_employment.get(db, id=id)
    if not user_employment:
        raise HTTPException(status_code=400, detail="User employment does not exists")
    response_data = schemas.UserEmployment.model_validate(user_employment)
    crud.user_employment.remove(db, id=id)
    return response_data
