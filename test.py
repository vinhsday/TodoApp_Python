from click import DateTime
from sqlalchemy import select

from database import Base, engine, SessionLocal
from models.new_task import Task
from datetime import *

from models.user import User
db = SessionLocal()

task = db.query(Task).filter(Task.id == 2).all()
for t in task:
    print((t.deadline - datetime.now()).days)