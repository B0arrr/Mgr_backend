from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Role(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
