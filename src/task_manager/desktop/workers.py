"""Reusable worker for executing blocking API calls outside the UI thread."""

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, QRunnable, Signal, Slot


class WorkerSignals(QObject):
    finished = Signal(object)
    failed = Signal(str)


class ApiWorker(QRunnable):
    """Run a callable in QThreadPool and emit its result or error."""

    def __init__(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = self.function(*self.args, **self.kwargs)
        except Exception as exc:  # The GUI presents backend errors to the user.
            self.signals.failed.emit(str(exc))
        else:
            self.signals.finished.emit(result)
