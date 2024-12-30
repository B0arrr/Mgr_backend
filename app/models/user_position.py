from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserPosition(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    position_id = Column(Integer, ForeignKey('position.id'))
    is_manager = Column(Boolean, default=False)

    users = relationship('User', back_populates='user_positions', viewonly=True)
    positions = relationship('Position', back_populates='user_positions', viewonly=True)
