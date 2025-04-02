from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.conf import containts
from src.conf import messages


class TodoSchema(BaseModel):
    title: str = Field(
        default=None,
        min_length=containts.TITLE_MIN_LENGTH,
        max_length=containts.TITLE_MAX_LENGTH,
        description=messages.todo_schema_title,
    )
    description: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=255,
        description=messages.todo_schema_description,
    )
    completed: Optional[bool] = Field(
        default=False, description=messages.todo_schema_completed
    )


class TodoSchemaUpdate(TodoSchema):
    model_config = ConfigDict(from_attributes=True)


class TodoUpdateStatusSchema(BaseModel):
    completed: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
