from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import UserWorkHour, UserWorkHourCreate, UserWorkHourUpdate

router = APIRouter(prefix="/user_workhour", tags=["user_workhour"])


@router.get("/", response_model=List[UserWorkHour])
async def get_user_workhours(db: SessionDep) -> Any:
    """
    Get all user workhours
    :param db: Database session
    :return: Returns all user workhours
    """
    return crud.user_work_hour.get_all(db)


@router.get("/{id}", response_model=UserWorkHour)
async def get_user_workhour(db: SessionDep, id: int) -> Any:
    """
    Get user workhour by id
    :param db: Database session
    :param id: ID of user workhour
    :return: Returns user workhour
    """
    user_workhour = crud.user_work_hour.get(db, id=id)
    if not user_workhour:
        raise HTTPException(status_code=404, detail="User workhour not found")
    return user_workhour


@router.post("/", response_model=UserWorkHour)
async def create_user_workhour(db: SessionDep, obj_in: UserWorkHourCreate) -> Any:
    """
    Create new user workhour
    :param db: Database session
    :param obj_in: User workhour object to create
    :return: Returns new user workhour
    """
    return crud.user_work_hour.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=UserWorkHour)
async def update_user_workhour(db: SessionDep, id: int, obj_in: UserWorkHourUpdate) -> Any:
    """
    Update user workhour by id
    :param db: Database session
    :param id: Id of user workhour
    :param obj_in: User workhour object to update
    :return: Returns updated user workhour
    """
    user_workhour = crud.user_work_hour.get(db, id=id)
    if not user_workhour:
        raise HTTPException(status_code=400, detail="User workhour does not exists")
    return crud.user_work_hour.update(db, db_obj=user_workhour, obj_in=obj_in)


@router.delete("/{id}", response_model=UserWorkHour)
async def delete_user_workhour(db: SessionDep, id: int) -> Any:
    """
    Delete user workhour by id
    :param db: Database session
    :param id: Id of user workhour
    :return: Returns deleted user workhour
    """
    user_workhour = crud.user_work_hour.get(db, id=id)
    if not user_workhour:
        raise HTTPException(status_code=400, detail="User workhour does not exists")
    return crud.user_work_hour.remove(db, id=id)
