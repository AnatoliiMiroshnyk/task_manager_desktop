# TaskFlow Desktop

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Qt](https://img.shields.io/badge/PySide6-Desktop_GUI-41CD52?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![Tests](https://github.com/AnatoliiMiroshnyk/task_manager_desktop/actions/workflows/tests.yml/badge.svg)](https://github.com/AnatoliiMiroshnyk/task_manager_desktop/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern desktop task manager with a PySide6 interface, a versioned FastAPI REST API, SQLAlchemy persistence, SQLite storage, background network workers, automated tests, and GitHub Actions CI.


## Features

- Modern dark desktop UI with sidebar filters, KPI cards, responsive table, search, and dialogs.
- Full task lifecycle: create, read, update, delete, filter, search, and overdue tracking.
- REST API with validation, OpenAPI documentation, pagination, and versioned routes.
- Layered architecture: API, service, repository, ORM, HTTP client, and presentation layers.
- Non-blocking GUI requests through Qt's thread pool.
- Isolated API, repository, HTTP-client, and Qt-model tests.
- One-command development launcher and CI workflow for Python 3.11–3.13.

## Screens and workflow

The application has three main areas:

1. **Sidebar** — filter all, to-do, in-progress, or completed tasks.
2. **Dashboard** — view total, status, and overdue KPI cards.
3. **Task table** — search, create, edit, and delete tasks; double-click a row to edit.

## Architecture

```text
Desktop GUI (PySide6)
        │ HTTP/JSON
        ▼
FastAPI /api/v1/tasks
        │
Service layer (business rules)
        │
Repository layer (queries)
        │
SQLAlchemy ORM → SQLite
```

```text
src/task_manager/
├── backend/
│   ├── api.py             # Versioned REST routes
│   ├── database.py        # Engine, sessions, table initialization
│   ├── main.py            # FastAPI factory and Uvicorn entry point
│   ├── models.py          # SQLAlchemy entities and enums
│   ├── repository.py      # Database CRUD and aggregate queries
│   ├── schemas.py         # Pydantic request/response contracts
│   └── service.py         # Business rules
├── desktop/
│   ├── api_client.py      # HTTP boundary and error mapping
│   ├── dialogs.py         # Create/edit task dialog
│   ├── main.py            # QApplication entry point
│   ├── main_window.py     # Dashboard composition and interactions
│   ├── models.py          # QAbstractTableModel
│   ├── styles.py          # Centralized modern dark theme
│   └── workers.py         # Background QRunnable API calls
└── __main__.py            # python -m task_manager
```

## Technology stack

| Area | Technology | Purpose |
|---|---|---|
| Desktop | PySide6 / Qt | Native Windows/Linux/macOS GUI |
| API | FastAPI + Uvicorn | Validated REST endpoints and OpenAPI docs |
| Data | SQLAlchemy 2 + SQLite | ORM persistence with zero local setup |
| Contracts | Pydantic 2 | Request and response validation |
| Networking | HTTPX | Desktop-to-API communication and API tests |
| Testing | pytest + pytest-qt | Backend, repository, client, and Qt tests |
| Quality | Ruff + GitHub Actions | Static checks and continuous integration |

## Requirements

- Python 3.11 or newer
- Windows 10/11, Linux, or macOS
- Git for version control

## Installation

```powershell
# Clone after creating your GitHub repository
git clone https://github.com/YOUR_USERNAME/taskflow-desktop.git
cd taskflow-desktop

# Windows PowerShell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

For a conventional requirements-file setup:

```powershell
pip install -r requirements.txt
pip install -e . --no-deps
```

## Quick start

The easiest development launch starts both the API and GUI:

```powershell
python run_dev.py
```

Alternatively, run each component in a separate terminal:

```powershell
# Terminal 1
.\.venv\Scripts\Activate.ps1
task-api

# Terminal 2
.\.venv\Scripts\Activate.ps1
task-desktop
```

API endpoints:

- Health: <http://127.0.0.1:8000/health>
- Swagger UI: <http://127.0.0.1:8000/docs>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

## API examples

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tasks   -H "Content-Type: application/json"   -d '{"title":"Prepare release","priority":"high","status":"todo","due_date":"2030-01-15"}'
```

Filter and search:

```bash
curl "http://127.0.0.1:8000/api/v1/tasks?status=todo&search=release"
```

## Tests and quality

```powershell
pytest
pytest --cov=task_manager --cov-report=term-missing
ruff check .
```

The suite uses an in-memory SQLite database, so it never modifies your local `data/taskflow.db`.

## Git workflow

Recommended incremental history:

```bash
git init
git branch -M main

git add pyproject.toml requirements.txt .gitignore LICENSE .env.example
git commit -m "chore: initialize TaskFlow project"

git add src/task_manager/backend
git commit -m "feat(api): implement FastAPI task CRUD and SQLite persistence"

git add src/task_manager/desktop
git commit -m "feat(gui): add modern PySide6 task dashboard"

git add tests
git commit -m "test: cover API repository client and Qt model"

git add .github run_dev.py README.md
git commit -m "ci: add test workflow and project documentation"
```

Create an empty repository named `taskflow-desktop` on GitHub, then push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/taskflow-desktop.git
git push -u origin main
```

Future work should use branches such as `feature/authentication`, `feature/postgresql`, or `fix/due-date-validation`, followed by a Pull Request into `main`.

## Roadmap

- JWT authentication and multi-user workspaces.
- Alembic database migrations and PostgreSQL deployment profile.
- Tags, projects, subtasks, recurring tasks, and reminders.
- Drag-and-drop Kanban board and system tray notifications.
- Docker Compose for API/database deployment.
- PyInstaller Windows installer and signed releases.

## Security and limitations

This portfolio edition binds the API to localhost and does not implement authentication. Do not expose it publicly without adding authentication, authorization, HTTPS, secrets management, database migrations, and production deployment controls.

## Contributing

1. Create a feature branch from `main`.
2. Add or update tests for changed behavior.
3. Run `pytest` and `ruff check .`.
4. Open a focused Pull Request with screenshots for UI changes.

## License

Distributed under the MIT License. See [LICENSE](LICENSE).
