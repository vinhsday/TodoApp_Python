import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean,default=False)
    deadline = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")
    description = Column(String, nullable=True)

    @property
    def days_remaining(self):
        if self.deadline is None:
            return
        return (self.deadline - datetime.today()).days
    
    @property
    def priority(self):
        if self.deadline is None:
            return "none"
        if self.days_remaining <= 2:
            return "high"
        elif self.days_remaining <= 10:
            return "medium"
        return "low"
    def rename(self, new_title):
            if not new_title.strip():
                raise ValueError("Title can't be empty")
            self.title = new_title.strip()

    def complete(self):
            self.completed = True

    

