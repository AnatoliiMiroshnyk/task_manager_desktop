"""Unit tests for repository queries and aggregate statistics."""

from datetime import date, timedelta

from task_manager.backend.models import TaskStatus
from task_manager.backend.repository import TaskRepository
from task_manager.backend.schemas import TaskCreate


def test_repository_filters_and_overdue_summary(session_factory):
    with session_factory() as session:
        repo = TaskRepository(session)
        repo.create(TaskCreate(title="Late task", due_date=date.today() - timedelta(days=1)))
        repo.create(TaskCreate(title="Finished task", status=TaskStatus.DONE, due_date=date.today() - timedelta(days=3)))

        assert len(repo.list(search="Late")) == 1
        assert len(repo.list(status=TaskStatus.DONE)) == 1
        summary = repo.summary()
        assert summary["total"] == 2
        assert summary["overdue"] == 1
