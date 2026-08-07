from click import DateTime
from sqlalchemy import select

from database import Base, engine, SessionLocal
from models.new_task import Task
from datetime import *

from models.user import User

Base.metadata.create_all(bind=engine)