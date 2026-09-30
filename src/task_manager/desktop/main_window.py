"""Main window composing TaskFlow's modern desktop interface."""

from functools import partial

from PySide6.QtCore import QTimer, QThreadPool, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from task_manager.desktop.api_client import TaskApiClient
from task_manager.desktop.dialogs import TaskDialog
from task_manager.desktop.models import TaskTableModel
from task_manager.desktop.workers import ApiWorker


class MainWindow(QMainWindow):
    """Task dashboard with async API operations and live filters."""

    def __init__(self, client: TaskApiClient | None = None) -> None:
        super().__init__()
        self.client = client or TaskApiClient()
        self.thread_pool = QThreadPool.globalInstance()
        self.current_status: str | None = None

        self.setWindowTitle("TaskFlow — Desktop Task Manager")
        self.resize(1240, 760)
        self.setMinimumSize(960, 620)
        self._build_ui()

        # Debounce search input to avoid an API request on every keystroke.
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(300)
        self.search_timer.timeout.connect(self.refresh)
        self.search_edit.textChanged.connect(lambda: self.search_timer.start())

        QTimer.singleShot(100, self.refresh)

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self._build_sidebar())
        root_layout.addWidget(self._build_content(), stretch=1)
        self.setCentralWidget(root)
        self.statusBar().showMessage("Connecting to API…")

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 24, 18, 18)
        layout.setSpacing(8)

        brand = QLabel("✓ TaskFlow")
        brand.setObjectName("brand")
        subtitle = QLabel("Focused work, clearly.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(24)

        self.nav_buttons = []
        for label, value in [
            ("All tasks", None), ("To do", "todo"),
            ("In progress", "in_progress"), ("Completed", "done")
        ]:
            button = QPushButton(label)
            button.setObjectName("nav")
            button.setCheckable(True)
            button.clicked.connect(partial(self._set_status_filter, value, button))
            self.nav_buttons.append(button)
            layout.addWidget(button)
        self.nav_buttons[0].setChecked(True)
        layout.addStretch()
        footer = QLabel("FastAPI + PySide6")
        footer.setObjectName("muted")
        layout.addWidget(footer)
        return sidebar

    def _build_content(self) -> QWidget:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 22)
        layout.setSpacing(18)

        title_row = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Task dashboard")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Plan, prioritize, and finish your work.")
        subtitle.setObjectName("muted")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        title_row.addLayout(title_box)
        title_row.addStretch()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search tasks…")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setFixedWidth(280)
        title_row.addWidget(self.search_edit)

        add_button = QPushButton("＋ New task")
        add_button.setObjectName("primary")
        add_button.clicked.connect(self.create_task)
        title_row.addWidget(add_button)
        layout.addLayout(title_row)

        cards = QHBoxLayout()
        self.card_values = {}
        for key, label in [
            ("total", "Total"), ("todo", "To do"), ("in_progress", "In progress"),
            ("done", "Done"), ("overdue", "Overdue")
        ]:
            card, value = self._metric_card(label)
            self.card_values[key] = value
            cards.addWidget(card)
        layout.addLayout(cards)

        self.table_model = TaskTableModel()
        self.table = QTableView()
        self.table.setModel(self.table_model)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for column in range(1, 5):
            self.table.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
        self.table.doubleClicked.connect(self.edit_task)
        layout.addWidget(self.table, stretch=1)

        actions = QHBoxLayout()
        actions.addStretch()
        refresh_button = QPushButton("↻ Refresh")
        refresh_button.clicked.connect(self.refresh)
        edit_button = QPushButton("Edit selected")
        edit_button.clicked.connect(self.edit_task)
        delete_button = QPushButton("Delete selected")
        delete_button.setObjectName("danger")
        delete_button.clicked.connect(self.delete_task)
        actions.addWidget(refresh_button)
        actions.addWidget(edit_button)
        actions.addWidget(delete_button)
        layout.addLayout(actions)
        return content

    @staticmethod
    def _metric_card(label: str) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(92)
        layout = QVBoxLayout(card)
        value = QLabel("—")
        value.setObjectName("cardValue")
        caption = QLabel(label)
        caption.setObjectName("cardLabel")
        layout.addWidget(value)
        layout.addWidget(caption)
        return card, value

    def _set_status_filter(self, status: str | None, selected: QPushButton) -> None:
        self.current_status = status
        for button in self.nav_buttons:
            button.setChecked(button is selected)
        self.refresh()

    def _selected_task(self) -> dict | None:
        indexes = self.table.selectionModel().selectedRows()
        return self.table_model.task_at(indexes[0].row()) if indexes else None

    def _run(self, function, on_success, *args) -> None:
        self.statusBar().showMessage("Working…")
        worker = ApiWorker(function, *args)
        worker.signals.finished.connect(on_success)
        worker.signals.failed.connect(self._show_error)
        self.thread_pool.start(worker)

    def refresh(self) -> None:
        search = self.search_edit.text().strip() or None
        self._run(self.client.list_tasks, self._tasks_loaded, self.current_status, search)
        self._run(self.client.summary, self._summary_loaded)

    def _tasks_loaded(self, tasks: list[dict]) -> None:
        self.table_model.replace(tasks)
        self.statusBar().showMessage(f"Loaded {len(tasks)} task(s)", 3000)

    def _summary_loaded(self, summary: dict) -> None:
        for key, label in self.card_values.items():
            label.setText(str(summary.get(key, 0)))

    def create_task(self) -> None:
        dialog = TaskDialog(parent=self)
        if dialog.exec():
            self._run(self.client.create_task, lambda _: self.refresh(), dialog.payload())

    def edit_task(self, *_args) -> None:
        task = self._selected_task()
        if task is None:
            QMessageBox.information(self, "Edit task", "Select a task first.")
            return
        dialog = TaskDialog(task, self)
        if dialog.exec():
            self._run(self.client.update_task, lambda _: self.refresh(), task["id"], dialog.payload())

    def delete_task(self) -> None:
        task = self._selected_task()
        if task is None:
            QMessageBox.information(self, "Delete task", "Select a task first.")
            return
        answer = QMessageBox.question(
            self, "Delete task", f"Delete ‘{task['title']}’? This action cannot be undone."
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._run(self.client.delete_task, lambda _: self.refresh(), task["id"])

    def _show_error(self, message: str) -> None:
        self.statusBar().showMessage("Request failed", 5000)
        QMessageBox.critical(
            self, "TaskFlow API error",
            f"{message} Make sure the backend is running on http://127.0.0.1:8000.",
        )
