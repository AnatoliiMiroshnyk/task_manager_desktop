"""Modal dialog for creating and editing tasks."""

from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)


class TaskDialog(QDialog):
    def __init__(self, task: dict | None = None, parent=None) -> None:
        super().__init__(parent)
        self.task = task
        self.setWindowTitle("Edit task" if task else "Create task")
        self.setMinimumWidth(480)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("What needs to be done?")
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Add context, acceptance criteria, or notes…")
        self.description_edit.setFixedHeight(120)

        self.status_combo = QComboBox()
        self.status_combo.addItem("To do", "todo")
        self.status_combo.addItem("In progress", "in_progress")
        self.status_combo.addItem("Done", "done")

        self.priority_combo = QComboBox()
        self.priority_combo.addItem("Low", "low")
        self.priority_combo.addItem("Medium", "medium")
        self.priority_combo.addItem("High", "high")

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.due_date_edit.setSpecialValueText("No due date")
        self.due_date_edit.setMinimumDate(QDate(2000, 1, 1))
        self.due_date_edit.setDate(QDate.currentDate())

        form = QFormLayout()
        form.addRow("Title *", self.title_edit)
        form.addRow("Description", self.description_edit)
        form.addRow("Status", self.status_combo)
        form.addRow("Priority", self.priority_combo)
        form.addRow("Due date", self.due_date_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        if task:
            self._populate(task)

    def _populate(self, task: dict) -> None:
        self.title_edit.setText(task["title"])
        self.description_edit.setPlainText(task.get("description", ""))
        self.status_combo.setCurrentIndex(self.status_combo.findData(task["status"]))
        self.priority_combo.setCurrentIndex(self.priority_combo.findData(task["priority"]))
        if task.get("due_date"):
            self.due_date_edit.setDate(QDate.fromString(task["due_date"], "yyyy-MM-dd"))

    def _validate_and_accept(self) -> None:
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Validation", "Task title is required.")
            return
        self.accept()

    def payload(self) -> dict:
        return {
            "title": self.title_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip(),
            "status": self.status_combo.currentData(),
            "priority": self.priority_combo.currentData(),
            "due_date": self.due_date_edit.date().toString("yyyy-MM-dd"),
        }
