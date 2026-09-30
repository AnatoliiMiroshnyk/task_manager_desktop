"""FastAPI routes for the task resource."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from task_manager.backend.database import get_session
from task_manager.backend.models import TaskStatus
from task_manager.backend.repository import TaskRepository
from task_manager.backend.schemas import TaskCreate, TaskRead, TaskSummary, TaskUpdate
from task_manager.backend.service import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
SessionDep = Annotated[Session, Depends(get_session)]


def build_service(session: Session) -> TaskService:
    return TaskService(TaskRepository(session))


@router.get("", response_model=list[TaskRead])
def list_tasks(
    session: SessionDep,
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    search: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    return build_service(session).list_tasks(status_filter, search, limit, offset)


@router.get("/summary", response_model=TaskSummary)
def get_summary(session: SessionDep):
    return build_service(session).get_summary()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep):
    return build_service(session).get_task(task_id)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, session: SessionDep):
    return build_service(session).create_task(payload)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, session: SessionDep):
    return build_service(session).update_task(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDep):
    build_service(session).delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
