from typing import Optional

from pydantic import BaseModel, ConfigDict


# Defines the data required to create a Todo.
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


# Defines the fields that can be updated.
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# Allows updating only the completion status.
class TodoStatusUpdate(BaseModel):
    completed: bool


# Defines the Todo data returned by the API.
class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Read attributes from SQLAlchemy models.

    id: int
    title: str
    description: Optional[str]
    completed: bool