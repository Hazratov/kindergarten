from app.core.celery import celery
from sqlalchemy.orm import sessionmaker
from app.core.database.config import get_sync_session_maker
from app.api.models.monthly_report import MonthlyReport
from app.api.models.meal_log import MealLog
from datetime import datetime
from sqlalchemy import extract

SyncSessionLocal: sessionmaker = get_sync_session_maker()


@celery.task
def generate_monthly_report(year: int, month: int, user_id: int):
    session = SyncSessionLocal()
    try:
        # 1. Hisobot ma'lumotlarini yig'ish
        total_portions = session.query(MealLog).filter(
            extract('year', MealLog.served_at) == year,
            extract('month', MealLog.served_at) == month,
            MealLog.status == "completed"
        ).count()

        # Bu yerda siz boshqa statistikalarni hisoblash qo'shishingiz mumkin:
        total_possible_portions = 1000  # misol uchun
        wastage_percentage = 5.0
        total_ingredients_used = 200.0
        total_cost = 1500.00
        efficiency_score = 95.0

        # 2. Hisobotni yaratish yoki yangilash
        report = session.query(MonthlyReport).filter_by(month=month, year=year).first()
        if not report:
            report = MonthlyReport(
                month=month,
                year=year,
                total_portions_served=total_portions,
                total_possible_portions=total_possible_portions,
                wastage_percentage=wastage_percentage,
                total_ingredients_used=total_ingredients_used,
                total_cost=total_cost,
                efficiency_score=efficiency_score,
                generated_at=datetime.utcnow(),
                generated_by=user_id
            )
            session.add(report)
        else:
            report.total_portions_served = total_portions
            report.total_possible_portions = total_possible_portions
            report.wastage_percentage = wastage_percentage
            report.total_ingredients_used = total_ingredients_used
            report.total_cost = total_cost
            report.efficiency_score = efficiency_score
            report.generated_at = datetime.utcnow()
            report.generated_by = user_id
        session.commit()
    finally:
        session.close()
