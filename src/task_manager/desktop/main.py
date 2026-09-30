"""Desktop application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from task_manager.desktop.main_window import MainWindow
from task_manager.desktop.styles import APP_STYLESHEET


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("TaskFlow")
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
