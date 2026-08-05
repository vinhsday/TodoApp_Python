from sqlalchemy import select

from database import Base, engine, SessionLocal
from models.new_task import Task
from datetime import *

from models.user import User
Base.metadata.create_all(bind=engine)

task = Task(
    title="Hello",
    completed=False,
    deadline=date(2026,12,12)
)
user = User(
    username="Helllo",
    hashed_password="123456"
)
