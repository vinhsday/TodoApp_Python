from pydantic import BaseModel


class CompleteRequest(BaseModel):
    completed: bool | None = None