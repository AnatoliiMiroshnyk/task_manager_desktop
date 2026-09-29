"""Pydantic request and response schemas.

Schemas validate data at the HTTP boundary and keep API contracts separate
from SQLAlchemy persistence models.
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from task_manager.backend.models import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=4000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = None


class TaskCreate(TaskBase):
    """Payload accepted when a new task is created."""


class TaskUpdate(BaseModel):
    """Partial-update payload. Omitted values remain unchanged."""

    title: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=4000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class TaskSummary(BaseModel):
    total: int
    todo: int
    in_progress: int
    done: int
    overdue: int
