from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: int

    model_config = {"from_attributes": True}
