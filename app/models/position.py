from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class Position(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
