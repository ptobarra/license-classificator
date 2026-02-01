from fastapi import FastAPI
from app.api.routes import router
from app.db.session import init_db


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Initializes the database schema and registers API routes for the
    License Classificator service. This factory function is used both
    for production deployment and testing.

    Returns:
        A configured FastAPI application instance with:
        - Database tables created via [`init_db`](app/db/session.py)
        - API routes registered from [`router`](app/api/routes.py)
        - Application metadata (title, version)

    Example:
        >>> app = create_app()
        >>> app.title
        'License Classificator'
        >>> app.version
        '1.0.0'

    Note:
        This function is called automatically when the module is imported,
        creating the global `app` instance used by Uvicorn. Database
        initialization happens on every application startup.
    """
    init_db()
    app = FastAPI(title="License Classificator", version="1.0.0")
    app.include_router(router)
    return app


app = create_app()
