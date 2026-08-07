from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///todo.db")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

from models.new_task import Task
from models.user import User

Base.metadata.create_all(bind=engine)