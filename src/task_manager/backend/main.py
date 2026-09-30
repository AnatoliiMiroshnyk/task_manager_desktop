"""FastAPI application factory and development server entry point."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from task_manager import __version__
from task_manager.backend.api import router
from task_manager.backend.database import create_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize required resources before accepting requests."""
    create_tables()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="TaskFlow API",
        version=__version__,
        description="REST API used by the TaskFlow desktop client.",
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    return app


app = create_app()


def run() -> None:
    """Run the backend with Uvicorn for local development."""
    uvicorn.run("task_manager.backend.main:app", host="127.0.0.1", port=8000, reload=False)
