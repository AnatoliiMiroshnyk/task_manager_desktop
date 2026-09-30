"""Smoke tests for the Qt task table model."""

from PySide6.QtCore import Qt

from task_manager.desktop.models import TaskTableModel


def test_table_model_displays_task(qtbot):
    model = TaskTableModel([
        {
            "id": 1,
            "title": "Write documentation",
            "description": "",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2030-01-01",
            "updated_at": "2026-09-23T12:00:00",
        }
    ])
    assert model.rowCount() == 1
    assert model.columnCount() == 5
    assert model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole) == "Write documentation"
    assert model.data(model.index(0, 1), Qt.ItemDataRole.DisplayRole) == "In Progress"
