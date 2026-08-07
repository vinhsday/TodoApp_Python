from datetime import date, datetime
import re
from signal import raise_signal
import stat
from sys import deactivate_stack_trampoline
from time import sleep
from turtle import reset
from sqlalchemy.orm import Session
from enums.priority import PriorityEnum
from models.new_task import Task
from sqlalchemy import *
from models.user import User
from schemas import TaskUpdate
from schemas.UserCreate import UserCreate
from security import verify_password, hash_password

class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def add_task(self, title: str, user: User,deadline: datetime|None=None) -> Task:
        try:
            task = Task(
                title=title,
                deadline=deadline
            )
            user.tasks.append(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception:
            self.db.rollback()
            raise 

    def get_tasks(self, 
                  user: User, 
                  completed: bool | None = None,
                  search: str | None = None,
                  sort: str | None = None) -> list[Task]:
        # statement = (
        #     select(Task)
        #     .where(Task.user_id == user.id)
        #     .order_by(Task.deadline)
        # ) 
        # result = self.db.execute(statement)
        # tasks = result.scalars().all()
        query = (
            self.db.query(Task)
            .filter(Task.user_id == user.id)
        )
        
        if completed is not None:
            query = query.filter(Task.completed == completed)


        if search:
            query = query.filter(Task.title.ilike(f"%{search}%"))

        allowed_sort = {
            "deadline": Task.deadline
        }
        
        if sort in allowed_sort:
            column = allowed_sort[sort]
            query = query.order_by(nulls_last(column.asc()))
        return query.all()

    def get_task(self, task_id, user: User):
        statement = (
            select(Task)
            .where(Task.id == task_id)
            .where(Task.user_id == user.id)
        )
        result = self.db.execute(statement)
        task = result.scalar_one_or_none()
        if task is None:
            raise IndexError("Task not found")
        return task

    def update_task(self, task_id: int, request: TaskUpdate, user: User) -> Task:
        task = self.get_task(task_id, user)
        data = request.model_dump(exclude_unset=True)
        for field,value in data.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int, user: User) -> Task:
        task = self.get_task(task_id, user)
        try: 
            self.db.delete(task)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise IndexError()
        return task
    # def get_user(self, user_id: int) -> User:
    #     statement = (
    #         select(User)
    #         .where(User.id==user_id)
    #     )
    #     result = self.db.execute(statement)
    #     user = result.scalar_one_or_none()
    #     if user is None:
    #         raise IndexError("User not found")
    #     return user
    # def get_users(self):
    #     statement = (
    #         select(User)
    #     )
    #     result = self.db.execute(statement)
    #     user = result.scalars().all()
    #     return user
    # def get_user_tasks(self, user_id: int):
    #     user = self.get_user(user_id)
    #     return user.tasks

    def add_user(self, user: UserCreate):
        user = User(
            username=user.username,
            password=user.password
        )
        self.db.add(user)
        self.db.commit()

    def register_user(self, user: UserCreate) -> User:
        """
        Create new user
        Check whether username exists or not before create
        """
        statement = (
            select(User)
            .where(User.username == user.username)
        )
        result = (self.db.execute(statement)).scalar_one_or_none()
        if result:
            raise ValueError("Username already exists")
            
        new_user = User(
            username=user.username,
            hashed_password=hash_password(user.password)
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def login(self, username: str, password: str) -> User:
        user = self.get_user_by_username(username)
        if user is None:
            raise ValueError("Invalid username or password")
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid username or password")
        return user

    def get_user_by_username(self, username):
        statement = (
            select(User)
            .where(User.username == username)
        )
        result = self.db.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise ValueError("Invalid username or password")
        return user

    def get_tasks_by_completed(self, user: User, completed):
        query = (
            self.db.query(Task)
            .filter(Task.user_id == user.id)
        )

        if completed is not None:
            query = query.filter(Task.completed == completed)

        return query.all()
