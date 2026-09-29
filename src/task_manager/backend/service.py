"""Application service layer.

Business rules live here instead of in API routes or GUI code. This separation
makes the behavior easy to test and keeps transport concerns independent.
"""

from fastapi import HTTPException, status

from task_manager.backend.models import Task, TaskStatus
from task_manager.backend.repository import TaskRepository
from task_manager.backend.schemas import TaskCreate, TaskSummary, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def list_tasks(
        self, status_filter: TaskStatus | None, search: str | None, limit: int, offset: int
    ) -> list[Task]:
        return self.repository.list(
            status=status_filter, search=search, limit=limit, offset=offset
        )

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    def create_task(self, payload: TaskCreate) -> Task:
        # Pydantic already validates length; strip whitespace as a domain rule.
        payload.title = payload.title.strip()
        if not payload.title:
            raise HTTPException(status_code=422, detail="Title cannot be blank")
        return self.repository.create(payload)

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        if payload.title is not None:
            payload.title = payload.title.strip()
            if not payload.title:
                raise HTTPException(status_code=422, detail="Title cannot be blank")
        return self.repository.update(task, payload)

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.repository.delete(task)

    def get_summary(self) -> TaskSummary:
        return TaskSummary(**self.repository.summary())
