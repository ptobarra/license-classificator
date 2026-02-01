from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Database engine using SQLite
engine = create_engine(f"sqlite:///{settings.sqlite_path}", echo=False)


def init_db() -> None:
    """
    Initialize the database schema by creating all SQLModel tables.

    Creates all tables defined in SQLModel models (e.g., [`License`](app/db/models.py))
    using the SQLite engine configured in [`settings.sqlite_path`](app/core/config.py).
    This function is idempotent - calling it multiple times will not duplicate tables.

    The function is automatically invoked during application startup in
    [`create_app`](app/main.py) to ensure the database schema exists before
    handling requests.

    Example:
        >>> from app.db.session import init_db
        >>> init_db()  # Creates License table if it doesn't exist

    Note:
        Uses the global [`engine`](app/db/session.py) instance. In production,
        consider using migration tools like Alembic for schema versioning.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    FastAPI dependency that provides a database session for request handling.

    Yields a SQLModel Session instance connected to the SQLite database configured
    in [`settings.sqlite_path`](app/core/config.py). The session is automatically
    committed and closed after the request completes, ensuring proper resource
    cleanup and transaction management.

    Yields:
        Session: Active SQLModel database session for executing queries

    Example:
        >>> from fastapi import Depends
        >>> from app.db.session import get_session
        >>> @app.get("/licenses")
        >>> def list_licenses(session: Session = Depends(get_session)):
        ...     return session.exec(select(License)).all()

    Note:
        Used as a FastAPI dependency in [`routes.py`](app/api/routes.py).
        The context manager ensures the session is properly closed even if
        an exception occurs during request processing.
    """
    with Session(engine) as session:
        yield session
