from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import ForeignKey, Float, String, Integer, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base, TimestampMixin


class ChangeType(PyEnum):
    delivery = "delivery"  # Yetkazib berish
    consumption = "consumption"  # Iste'mol
    waste = "waste"  # Isrof
    adjustment = "adjustment"  # Tuzatish


class InventoryLog(Base, TimestampMixin):
    __tablename__ = "inventory_logs"

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"), nullable=False
    )
    change_amount: Mapped[float] = mapped_column(Float, nullable=False)
    change_type: Mapped[ChangeType] = mapped_column(Enum(ChangeType), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    reference_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    changed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    previous_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    new_quantity: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="inventory_logs"
    )
    changed_by_user: Mapped["User"] = relationship(
        "User", back_populates="inventory_logs"
    )

    def __repr__(self) -> str:
        return f"<InventoryLog(ingredient_id={self.ingredient_id}, change={self.change_amount}, type='{self.change_type.value}')>"