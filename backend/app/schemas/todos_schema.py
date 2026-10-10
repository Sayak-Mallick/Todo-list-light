from uuid import UUID

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(BaseModel):
    title: str
    description: str
    is_completed: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
