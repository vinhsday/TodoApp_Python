from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    completed: bool
    deadline: datetime | None = None
    priority: str
    user_id: int