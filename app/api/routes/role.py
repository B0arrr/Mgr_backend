from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import Role, User, RoleCreate, RoleUpdate

router = APIRouter(prefix="/role", tags=["role"])


@router.get("/", response_model=List[Role])
async def get_roles(db: SessionDep) -> Any:
    """
    Get all roles
    :param db: Database connection
    :return: Returns all roles
    """
    return crud.role.get_all(db)


@router.get("/{id}", response_model=Role)
async def get_role(db: SessionDep, id: int) -> Any:
    """
    Get a role
    :param db: Database connection
    :param id: Id of the role
    :return: Returns role
    """
    role = crud.role.get(db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("/{id}/users", response_model=List[User])
async def get_users_with_role(db: SessionDep, id: int) -> Any:
    """
    Get all users with role
    :param db: Database connection
    :param id: Id of the role
    :return: Returns all users
    """
    role = crud.role.get(db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role.users


@router.post("/", response_model=Role)
async def create_role(db: SessionDep, obj_in: RoleCreate) -> Any:
    """
    Create a new role
    :param db: Database connection
    :param obj_in: Role object to create
    :return: Returns new role
    """
    role = crud.role.get_by_name(db, name=obj_in.name)
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.role.create(db, obj_in=obj_in)


@router.put("/{id}", response_model=Role)
async def update_role(db: SessionDep, id: int, obj_in: RoleUpdate) -> Any:
    """
    Update a role
    :param db: Database connection
    :param id: Id of the role
    :param obj_in: Role object to update
    :return: Returns updated role
    """
    role = crud.role.get(db, id=id)
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exists")
    return crud.role.update(db, db_obj=role, obj_in=obj_in)


@router.delete("/{id}", response_model=Role)
async def delete_role(db: SessionDep, id: int) -> Any:
    """
    Delete a role
    :param db: Database connection
    :param id: Id of the role
    :return: Returns deleted role
    """
    role = crud.role.get(db, id=id)
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exists")
    return crud.role.remove(db, id=id)
