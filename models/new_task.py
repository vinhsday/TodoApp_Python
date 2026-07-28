from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base
from datetime import date
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean,default=False)
    deadline = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")

    @property
    def days_remaining(self):
        return (self.deadline - date.today()).days
    @property
    def priority(self):
        if self.days_remaining <= 2:
            return "red"
        elif self.days_remaining <= 10:
            return "yellow"
        return "green"
    def rename(self, new_title):
            if not new_title.strip():
                raise ValueError("Title can't be empty")
            self.title = new_title.strip()

    def complete(self):
            self.completed = True

