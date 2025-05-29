from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.api.models.meal_log import MealLog


class MealLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[MealLog]:
        result = await self.session.execute(select(MealLog))
        return result.scalars().all()

    async def get_by_id(self, meal_log_id: int) -> Optional[MealLog]:
        result = await self.session.execute(
            select(MealLog).where(MealLog.id == meal_log_id)
        )
        return result.scalar_one_or_none()

    async def create(self, meal_log: MealLog) -> MealLog:
        self.session.add(meal_log)
        await self.session.commit()
        await self.session.refresh(meal_log)
        return meal_log

    async def delete(self, meal_log: MealLog) -> None:
        await self.session.delete(meal_log)
        await self.session.commit()
