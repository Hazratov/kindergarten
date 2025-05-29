from app.core.celery import celery
from app.api.models.inventory_log import InventoryLog
from app.api.models.notification import Notification, NotificationType, NotificationPriority
from sqlalchemy.orm import sessionmaker
from app.core.database.config import get_sync_session_maker
from datetime import datetime


SyncSessionLocal: sessionmaker = get_sync_session_maker()

@celery.task
def process_inventory_log(log_id: int):
    session = SyncSessionLocal()
    try:
        log = session.query(InventoryLog).filter(InventoryLog.id == log_id).first()
        if not log:
            return

        # Masalan, ingredient miqdori 10 dan kam bo'lsa ogohlantirish yaratish
        if log.new_quantity < 10:
            notification = Notification(
                user_id=log.changed_by,
                title="Ingredient quantity low",
                message=f"Ingredient ID {log.ingredient_id} quantity is low: {log.new_quantity}g",
                type=NotificationType.warning,
                priority=NotificationPriority.high,
                is_read=False,
                is_system_generated=True,
                created_at=datetime.utcnow()
            )
            session.add(notification)
            session.commit()
    finally:
        session.close()
