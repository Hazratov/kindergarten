from app.core.celery import celery
from app.api.models.notification import Notification
from app.core.database.config import get_sync_session_maker
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.api.websocket.connection_manager import manager
import json

SyncSessionLocal: sessionmaker = get_sync_session_maker()


@celery.task
def create_system_notification(user_id: int, title: str, message: str, notif_type: str = "info", priority: str = "medium"):
    session = SyncSessionLocal()
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notif_type,
            priority=priority,
            is_read=False,
            is_system_generated=True,
            created_at=datetime.utcnow()
        )
        session.add(notification)
        session.commit()

        # WebSocket orqali jonli xabar yuborish (sinxron emas, uni alohida async-da chaqirish kerak)
        # Shu yerda faqat oddiy signal yuborilishi mumkin, lekin to‘liq WebSocket uchun alohida async funksiya kerak

    finally:
        session.close()
