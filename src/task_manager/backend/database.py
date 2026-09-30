"""Database configuration and session lifecycle.

The application uses SQLite for a zero-configuration local setup. The database
URL can be replaced later with PostgreSQL without changing the service layer.
"""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_PATH = Path("data/taskflow.db")
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


class Base(DeclarativeBase):
    """Base class used by all SQLAlchemy ORM models."""


def create_session_factory(database_url: str = DATABASE_URL) -> sessionmaker[Session]:
    """Create a session factory for the supplied database URL.

    ``check_same_thread=False`` is required because FastAPI may use SQLite
    connections from different worker threads.
    """
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, connect_args=connect_args)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


SessionLocal = create_session_factory()
engine = SessionLocal.kw["bind"]


def create_tables() -> None:
    """Create all registered database tables."""
    from task_manager.backend import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that provides one database session per request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
