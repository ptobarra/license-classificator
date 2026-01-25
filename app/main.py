from fastapi import FastAPI
from app.api.routes import router
from app.db.session import init_db


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(title="License Classificator", version="1.0.0")
    app.include_router(router)
    return app


app = create_app()
