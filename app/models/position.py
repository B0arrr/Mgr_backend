from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Position(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)

    users_positions = relationship("UsersPosition", back_populates="positions")
    users = relationship("Users", secondary="userposition", back_populates="positions")
