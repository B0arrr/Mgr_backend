from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import Department, DepartmentCreate, DepartmentUpdate, User

router = APIRouter(prefix="/department", tags=["department"])


@router.get("/", response_model=List[Department])
async def get_departments(db: SessionDep) -> Any:
    """
    Get all departments
    :param db: Database session
    :return: Returns all departments
    """
    return crud.department.get_all(db)


@router.get("/{id}", response_model=Department)
async def get_department(db: SessionDep, id: int) -> Any:
    """
    Get department by id
    :param db: Database session
    :param id: Id of the department
    :return: Returns department by id
    """
    department = crud.department.get(db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.get("/{id}/users", response_model=List[User])
async def get_users_from_department(db: SessionDep, id: int) -> Any:
    """
    Get all users from department
    :param db: Database session
    :param id: Id of the department
    :return: Returns users from department
    """
    department = crud.department.get(db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.users


@router.post("/", response_model=Department)
async def create_department(db: SessionDep, obj_in: DepartmentCreate) -> Any:
    """
    Create new department
    :param db: Database session
    :param obj_in: Department object to create
    :return: Returns created department
    """
    department = crud.department.get_by_name(db, name=obj_in.name)
    if department:
        raise HTTPException(status_code=400, detail="Department already exists")
    return crud.department.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=Department)
async def update_department(db: SessionDep, id: int, obj_in: DepartmentUpdate) -> Any:
    """
    Update department by id
    :param db: Database session
    :param id: Id of the department
    :param obj_in: Department object to update
    :return: Returns updated department
    """
    department = crud.department.get(db, id=id)
    if not department:
        raise HTTPException(status_code=400, detail="Department does not exists")
    return crud.department.update(db, db_obj=department, obj_in=obj_in)


@router.delete("/{id}", response_model=Department)
async def delete_department(db: SessionDep, id: int) -> Any:
    """
    Delete department by id
    :param db: Database session
    :param id: Id of the department
    :return: Returns deleted department
    """
    department = crud.department.get(db, id=id)
    if not department:
        raise HTTPException(status_code=400, detail="Department does not exists")
    return crud.department.remove(db, id=id)
