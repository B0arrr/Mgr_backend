from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Role(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)

    user_roles = relationship("UserRole", back_populates="roles")
    users = relationship("User", secondary="userrole", back_populates="roles")
