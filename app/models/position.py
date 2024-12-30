from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Position(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)

    user_positions = relationship("UserPosition", back_populates="positions", viewonly=True)
    users = relationship("User", secondary="userposition", back_populates="positions")
