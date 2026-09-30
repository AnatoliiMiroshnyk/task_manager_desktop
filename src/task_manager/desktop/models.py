"""Qt model used by the desktop task table."""

from datetime import date
from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QFont


class TaskTableModel(QAbstractTableModel):
    HEADERS = ["Task", "Status", "Priority", "Due date", "Updated"]

    def __init__(self, tasks: list[dict] | None = None) -> None:
        super().__init__()
        self._tasks = tasks or []

    def rowCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return len(self._tasks)

    def columnCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        task = self._tasks[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            values = [
                task["title"],
                task["status"].replace("_", " ").title(),
                task["priority"].title(),
                task.get("due_date") or "—",
                task["updated_at"][:10],
            ]
            return values[column]

        if role == Qt.ItemDataRole.ForegroundRole:
            if column == 1:
                return QColor({"todo": "#94a3b8", "in_progress": "#38bdf8", "done": "#34d399"}[task["status"]])
            if column == 2:
                return QColor({"low": "#a7f3d0", "medium": "#fbbf24", "high": "#fb7185"}[task["priority"]])
            if column == 3 and task.get("due_date") and task["status"] != "done":
                if date.fromisoformat(task["due_date"]) < date.today():
                    return QColor("#fb7185")

        if role == Qt.ItemDataRole.FontRole and column == 0:
            font = QFont()
            font.setBold(True)
            return font
        return None

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:  # noqa: N802
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def replace(self, tasks: list[dict]) -> None:
        self.beginResetModel()
        self._tasks = list(tasks)
        self.endResetModel()

    def task_at(self, row: int) -> dict:
        return self._tasks[row]
