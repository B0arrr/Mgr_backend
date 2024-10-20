from sqlalchemy import Column, Integer, ForeignKey, Boolean

from app.db.base_class import Base


class UserPositions(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))
    is_manager = Column(Boolean, default=False)
