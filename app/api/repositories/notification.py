from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.api.models.notification import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_for_user(self, user_id: int) -> List[Notification]:
        result = await self.session.execute(
            select(Notification).where(Notification.user_id == user_id)
        )
        return result.scalars().all()

    async def create(self, notification: Notification) -> Notification:
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def mark_as_read(self, notification_id: int) -> None:
        notification = await self.session.get(Notification, notification_id)
        if notification:
            notification.is_read = True
            self.session.add(notification)
            await self.session.commit()
