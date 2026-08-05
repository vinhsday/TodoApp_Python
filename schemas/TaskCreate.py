from pydantic import BaseModel
from datetime import date, datetime
class TaskCreate(BaseModel):
    title: str
    deadline: datetime | None = None
