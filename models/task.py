from datetime import datetime
from database import Base
from sqlalchemy import Column
from datetime import date
class Task:
    def __init__(self, title, completed = False, created_at = None, deadline = None):
        if created_at == None:
            created_at = datetime.strptime(datetime.now().strftime("%Y-%m-%d"),"%Y-%m-%d")
        if not title.strip():
            raise ValueError(...)
        if isinstance(deadline, str):
            deadline = datetime.strptime(deadline, "%Y-%m-%d")
        
        self.title = title
        self.completed = completed
        self.created_at = created_at
        self.deadline = self.create_deadline(deadline)
        self.days_remaining = abs((self.created_at - self.deadline).days)
        self.priority = self.prioritize()

    def __str__(self):
        tick = "[x]" if self.completed else "[ ]"
        return f"{tick} {self.title} (deadline={self.deadline} priority={self.priority} days_remaining={self.days_remaining})"
    
    def rename(self, new_title):
        if not new_title.strip():
            raise ValueError("Title can't be empty")
        self.title = new_title.strip()
    
    def toggle(self):
        self.completed = not self.completed
    
    def complete(self):
        self.completed = True

    def prioritize(self):
        days_gap = abs((self.created_at - self.deadline).days)
        if days_gap <= 2:
            return "Red"
        elif days_gap <= 10:
            return "Yellow"
        
        return "Green"

    def create_deadline(self, deadline: datetime):
        if deadline.month < self.created_at.month:
            raise ValueError()
        elif deadline.month == self.created_at.month:
            if deadline.day < self.created_at.day:
                raise ValueError()
        self.deadline = deadline
        return deadline

    def calculate_days_remaining(self):
        self.days_remaining = abs((self.created_at - self.deadline).days)

 

