from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import UserSchedule, UserScheduleCreate, UserScheduleUpdate

router = APIRouter(prefix="/user_schedule", tags=["user_schedule"])


@router.get("/", response_model=List[UserSchedule])
async def get_user_schedules(db: SessionDep) -> Any:
    """
    Get all users schedule
    :param db: Database session
    :return: Returns all user schedule
    """
    return crud.user_schedule.get_all(db)


@router.get("/{id}", response_model=UserSchedule)
async def get_user_schedule(db: SessionDep, id: int) -> Any:
    """
    Get user schedule by id
    :param db: Database session
    :param id: Id of the user schedule
    :return: Returns user schedule
    """
    user_schedule = crud.user_schedule.get(db, id=id)
    if not user_schedule:
        raise HTTPException(status_code=404, detail="User schedule not found")
    return user_schedule


@router.post("/", response_model=UserSchedule)
async def create_user_schedule(db: SessionDep, obj_in: UserScheduleCreate) -> Any:
    """
    Create new user schedule
    :param db: Database session
    :param obj_in: User schedule object to create
    :return: Returns new user schedule
    """
    return crud.user_schedule.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=UserSchedule)
async def update_user_schedule(db: SessionDep, id: int, obj_in: UserScheduleUpdate) -> Any:
    """
    Update user schedule by id
    :param db: Database session
    :param id: Id of the user schedule
    :param obj_in: User schedule object to update
    :return: Returns updated user schedule
    """
    user_schedule = crud.user_schedule.get(db, id=id)
    if not user_schedule:
        raise HTTPException(status_code=400, detail="User schedule does not exists")
    return crud.user_schedule.update(db, db_obj=user_schedule, obj_in=obj_in)


@router.delete("/{id}", response_model=UserSchedule)
async def delete_user_schedule(db: SessionDep, id: int) -> Any:
    """
    Delete user schedule by id
    :param db: Database session
    :param id: Id of the user schedule
    :return: Returns deleted user schedule
    """
    user_schedule = crud.user_schedule.get(db, id=id)
    if not user_schedule:
        raise HTTPException(status_code=400, detail="User schedule does not exists")
    return crud.user_schedule.remove(db, id=id)
