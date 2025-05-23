from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import get_settings
from app.api.views.auth import router as auth_router

settings = get_settings()


def create_app() -> CORSMiddleware:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    app_.include_router(auth_router)
    return CORSMiddleware(
        app_,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )