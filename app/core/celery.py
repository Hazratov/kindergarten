from celery import Celery
from app.core.settings import get_settings

settings = get_settings()

celery = Celery(
    "celery_worker",
    broker=settings.GET_REDIS_URL,
    backend=settings.GET_REDIS_URL,
    include=[
        "app.api.tasks.inventory_tasks",
        "app.api.tasks.monthly_reports",
        "app.api.tasks.notifications"
        # boshqa task modullar ro'yxati
    ],
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)
