from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base


class MealStatus(PyEnum):
    completed = "completed"
    cancelled = "cancelled"


class MealLog(Base):
    __tablename__ = "meal_logs"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="RESTRICT"), nullable=False
    )
    served_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    portions_served: Mapped[int] = mapped_column(Integer, nullable=False)
    served_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    children_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[MealStatus] = mapped_column(
        Enum(MealStatus), default=MealStatus.completed
    )

    # Relationships
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="meal_logs")
    served_by_user: Mapped["User"] = relationship("User", back_populates="meal_logs")

    def __repr__(self) -> str:
        return f"<MealLog(recipe_id={self.recipe_id}, portions={self.portions_served}, status='{self.status.value}')>"
