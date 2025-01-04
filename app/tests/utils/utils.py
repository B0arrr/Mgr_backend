import random
import string
from datetime import date
from typing import List

from sqlalchemy.orm import Session

from app import crud
from app.core.security import get_password_hash
from app.models import User, Address, Company, Department, Employment, Position, Role, UserAddress, UserEmployment, \
    UserManager, UserRole
from app.schemas import UserAddressCreate, UserEmploymentCreate, UserManagerCreate, UserRoleCreate
from app.tests.utils.address import create_random_address
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.role import create_random_role
from app.tests.utils.user import create_random_user


def random_lower_string(amount: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=amount))


def random_email() -> str:
    return f"{random_lower_string(10)}@{random_lower_string(5)}.com"


def random_password() -> str:
    return get_password_hash(random_lower_string(8))


def random_int(min: int = 1, max: int = 100) -> int:
    return random.randint(min, max)


def random_bool() -> bool:
    return bool(random.getrandbits(1))


class TestRelationshipsHelper:
    user: List[User]
    managers: List[User]
    address: List[Address]
    company: List[Company]
    department: List[Department]
    employment: List[Employment]
    position: List[Position]
    role: List[Role]
    user_address: List[UserAddress]
    user_employment: List[UserEmployment]
    user_manager: List[UserManager]
    user_role: List[UserRole]

    @classmethod
    def setup_class(cls, db: Session):
        cls.user = [create_random_user(db) for _ in range(5)]
        cls.managers = [create_random_user(db) for _ in range(2)]
        cls.address = [create_random_address(db) for _ in range(5)]
        cls.company = [create_random_company(db) for _ in range(5)]
        cls.department = [create_random_department(db) for _ in range(5)]
        cls.employment = [create_random_employment(db) for _ in range(5)]
        cls.position = [create_random_position(db) for _ in range(5)]
        cls.role = [create_random_role(db) for _ in range(5)]
        user_address_tmp = [
            UserAddressCreate(
                user_id=random.choice(cls.user).id,
                address_id=random.choice(cls.address).id,
                is_remote=random_bool(),
            ) for _ in range(10)
        ]
        user_employment_tmp = [
            UserEmploymentCreate(
                user_id=random.choice(cls.user).id,
                employment_id=random.choice(cls.employment).id,
                company_id=random.choice(cls.company).id,
                department_id=random.choice(cls.department).id,
                position_id=random.choice(cls.position).id,
                start_date=date.today()
            ) for _ in range(10)
        ]
        user_manager_tmp = [
            UserManagerCreate(
                user_id=usr.id,
                manager_id=random.choice(cls.managers).id,
            ) for usr in cls.user
        ]
        user_role_tmp = [
            UserRoleCreate(
                user_id=usr.id,
                role_id=random.choice(cls.role).id,
            )
            for usr in cls.user
            for _ in range(random_int(max=5))
        ]
        cls.user_address = [crud.user_address.create(db, obj_in=address) for address in user_address_tmp]
        cls.user_employment = [crud.user_employment.create(db, obj_in=employment) for employment in user_employment_tmp]
        cls.user_manager = [crud.user_manager.create(db, obj_in=item) for item in user_manager_tmp]
        cls.user_role = [crud.user_role.create(db, obj_in=item) for item in user_role_tmp]
