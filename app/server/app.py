from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import get_settings
from app.api.views.auth import router as auth_router
from app.api.views.users import router as users_router
from app.api.views.ingredients import router as ingredients_router
from app.api.views.recipes import router as recipes_router
from app.api.views.inventory_log import router as inventory_log_router
from app.api.views.websocket import router as websocket_router
from app.api.views.meals import router as meals_router
from app.api.views.monthly_reports import router as monthly_reports_router
from app.api.views.notifications import router as notifications_router

settings = get_settings()


def create_app() -> CORSMiddleware:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    app_.include_router(auth_router)
    app_.include_router(users_router)
    app_.include_router(ingredients_router)
    app_.include_router(recipes_router)
    app_.include_router(inventory_log_router)
    app_.include_router(websocket_router)
    app_.include_router(meals_router)
    app_.include_router(monthly_reports_router)
    app_.include_router(notifications_router)


    return CORSMiddleware(
        app_,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )