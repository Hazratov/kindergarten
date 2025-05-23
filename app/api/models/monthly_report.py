from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, Integer, Float, DateTime, DECIMAL, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base


class MonthlyReport(Base):
    __tablename__ = "monthly_reports"

    month: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-12
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    total_portions_served: Mapped[int] = mapped_column(Integer, default=0)
    total_possible_portions: Mapped[int] = mapped_column(Integer, default=0)
    wastage_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    total_ingredients_used: Mapped[float] = mapped_column(Float, default=0.0)  # kg
    total_cost: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    efficiency_score: Mapped[float] = mapped_column(Float, default=0.0)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    generated_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    # Relationships
    generated_by_user: Mapped["User"] = relationship(
        "User", back_populates="monthly_reports"
    )

    # Unique constraint for month-year combination
    __table_args__ = (
        UniqueConstraint('month', 'year', name='_month_year_uc'),
    )

    @property
    def is_wastage_high(self) -> bool:
        """Check if wastage percentage is above 15%"""
        return self.wastage_percentage > 15.0

    def __repr__(self) -> str:
        return f"<MonthlyReport(month={self.month}, year={self.year}, wastage={self.wastage_percentage}%)>"