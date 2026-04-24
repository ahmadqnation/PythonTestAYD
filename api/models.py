from pydantic import BaseModel, Field, field_validator
from typing import Optional
import html


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    completed: bool = False

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, v: str) -> str:
        return html.escape(v.strip())


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, v: str) -> str:
        return html.escape(v.strip())


class Todo(TodoBase):
    id: int

    model_config = {"from_attributes": True}
