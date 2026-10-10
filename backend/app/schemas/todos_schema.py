from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool | None = None


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # this line is used to

    id: int
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
