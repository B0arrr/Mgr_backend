from typing import List, Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import Company, CompanyCreate, CompanyUpdate, User, CompanyDeleted

router = APIRouter(prefix="/company", tags=["company"])


@router.get("/", response_model=List[Company])
async def get_companies(db: SessionDep) -> Any:
    """
    Get all companies
    :param db: Database session
    :return: Returns all companies
    """
    return crud.company.get_all(db)


@router.get("/{company_id}", response_model=Company)
async def get_company(db: SessionDep, company_id: int) -> Any:
    """
    Get a company by id
    :param db: Database session
    :param company_id: Id of the company
    :return: Returns company by id
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/{company_id}/users", response_model=List[User])
async def get_users_from_company(db: SessionDep, company_id: int) -> Any:
    """
    Get all users from a company
    :param db: Database session
    :param company_id: Id of the company
    :return: Returns all users from a company
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company.users


@router.post("/", response_model=Company)
async def create_company(db: SessionDep, obj_in: CompanyCreate) -> Any:
    """
    Create a company
    :param db: Database session
    :param obj_in: Company object to create
    :return: Returns created company
    """
    company = crud.company.get_by_name(db, name=obj_in.name)
    if company:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.company.create(db, obj_in=obj_in)


@router.put("/{company_id}", response_model=Company)
async def update_company(db: SessionDep, company_id: int, obj_in: CompanyUpdate) -> Any:
    """
    Update a company
    :param db: Database session
    :param company_id: Id of the company
    :param obj_in: Company object to update
    :return: Returns updated company
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=400, detail="Company does not exists")
    return crud.company.update(db, db_obj=company, obj_in=obj_in)


@router.delete("/{company_id}", response_model=CompanyDeleted)
async def delete_company(db: SessionDep, company_id: int) -> Any:
    """
    Delete a company
    :param db: Database session
    :param company_id: Id of the company
    :return: Returns deleted company
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=400, detail="Company do not exists")
    return crud.company.remove(db, id=company_id)
