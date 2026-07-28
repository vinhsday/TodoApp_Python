from sqlalchemy.orm import relationship
from sqlalchemy import *
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    tasks = relationship('Task',back_populates="user")