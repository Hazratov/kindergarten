from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.api.models.inventory_log import InventoryLog


class InventoryLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[InventoryLog]:
        result = await self.session.execute(select(InventoryLog))
        return result.scalars().all()

    async def get_by_id(self, log_id: int) -> Optional[InventoryLog]:
        result = await self.session.execute(
            select(InventoryLog).where(InventoryLog.id == log_id)
        )
        return result.scalar_one_or_none()

    async def create(self, log: InventoryLog) -> InventoryLog:
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def delete(self, log: InventoryLog) -> None:
        await self.session.delete(log)
        await self.session.commit()
