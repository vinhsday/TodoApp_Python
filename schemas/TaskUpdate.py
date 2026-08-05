from pydantic import BaseModel
from datetime import date, datetime
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    deadline: datetime | None = None
