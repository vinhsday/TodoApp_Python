from datetime import date
from pydantic import BaseModel, ConfigDict

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    completed: bool
    deadline: date
    priority: str
    user_id: int