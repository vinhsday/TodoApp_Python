from pydantic import BaseModel
from datetime import date, datetime
class TaskCreate(BaseModel):
    title: str | None = None
    deadline: date | None = None
    complete: bool | None = None 
