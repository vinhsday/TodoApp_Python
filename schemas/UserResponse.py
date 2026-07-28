from pydantic import BaseModel, ConfigDict

from schemas.TaskResponse import TaskResponse


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    tasks: list[TaskResponse]