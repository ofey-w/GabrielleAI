from fastapi import FastAPI
from gabrielle.config import Settings
from gabrielle.api.routes import health


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.include_router(health.router)

    return app
