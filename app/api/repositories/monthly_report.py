from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.api.models.monthly_report import MonthlyReport


class MonthlyReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[MonthlyReport]:
        result = await self.session.execute(select(MonthlyReport))
        return result.scalars().all()

    async def get_by_month_year(self, month: int, year: int) -> Optional[MonthlyReport]:
        result = await self.session.execute(
            select(MonthlyReport).where(
                MonthlyReport.month == month,
                MonthlyReport.year == year
            )
        )
        return result.scalar_one_or_none()

    async def create(self, report: MonthlyReport) -> MonthlyReport:
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def update(self, report: MonthlyReport, data: dict) -> MonthlyReport:
        for key, value in data.items():
            setattr(report, key, value)
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report
