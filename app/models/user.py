from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base
class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)