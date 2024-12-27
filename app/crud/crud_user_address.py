from app.crud.base import CRUDBase
from app.models import UserAddress
from app.schemas import UserAddressCreate, UserAddressUpdate


class CRUDUserAddress(CRUDBase[UserAddress, UserAddressCreate, UserAddressUpdate]):
    pass


user_address = CRUDUserAddress(UserAddress)
