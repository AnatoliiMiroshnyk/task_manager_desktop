"""Repository layer containing database-specific CRUD operations."""

from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from task_manager.backend.models import Task, TaskStatus
from task_manager.backend.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    """Encapsulates SQLAlchemy queries for tasks."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        *,
        status: TaskStatus | None = None,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Task]:
        statement = select(Task)
        if status is not None:
            statement = statement.where(Task.status == status)
        if search:
            term = f"%{search.strip()}%"
            statement = statement.where(
                or_(Task.title.ilike(term), Task.description.ilike(term))
            )
        statement = statement.order_by(Task.created_at.desc()).limit(limit).offset(offset)
        return list(self.session.scalars(statement))

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def create(self, payload: TaskCreate) -> Task:
        task = Task(**payload.model_dump())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: Task, payload: TaskUpdate) -> Task:
        # exclude_unset distinguishes omitted fields from intentionally supplied values.
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def summary(self) -> dict[str, int]:
        total = self.session.scalar(select(func.count(Task.id))) or 0
        counts = {
            status.value: self.session.scalar(
                select(func.count(Task.id)).where(Task.status == status)
            ) or 0
            for status in TaskStatus
        }
        overdue = self.session.scalar(
            select(func.count(Task.id)).where(
                Task.due_date < date.today(), Task.status != TaskStatus.DONE
            )
        ) or 0
        return {
            "total": total,
            "todo": counts[TaskStatus.TODO.value],
            "in_progress": counts[TaskStatus.IN_PROGRESS.value],
            "done": counts[TaskStatus.DONE.value],
            "overdue": overdue,
        }
