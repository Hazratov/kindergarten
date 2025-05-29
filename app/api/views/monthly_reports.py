from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.core.database.config import get_general_session
from app.api.repositories.monthly_report import MonthlyReportRepository
from app.api.schemas.monthly_report import MonthlyReportResponse
from app.core.security import get_current_active_user
from app.api.models.user import User
from app.api.tasks.monthly_reports import generate_monthly_report

router = APIRouter(prefix="/monthly-reports", tags=["MonthlyReports"])


@router.get("/", response_model=List[MonthlyReportResponse])
async def get_monthly_reports(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    # Faqat admin va manager ko‘ra oladi
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    repo = MonthlyReportRepository(session)
    reports = await repo.get_all()
    return reports


@router.get("/{year}/{month}", response_model=MonthlyReportResponse)
async def get_monthly_report(
    year: int,
    month: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    repo = MonthlyReportRepository(session)
    report = await repo.get_by_month_year(month=month, year=year)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def trigger_generate_monthly_report(
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    # Celery taskni fon rejimida ishga tushurish
    generate_monthly_report.delay(year, month, current_user.id)

    return {"message": f"Monthly report generation for {month}/{year} triggered."}
