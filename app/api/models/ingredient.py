from datetime import date
from decimal import Decimal
from sqlalchemy import String, Float, Date, Boolean, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base, TimestampMixin


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    quantity_grams: Mapped[float] = mapped_column(Float, default=0.0)
    minimum_threshold: Mapped[float] = mapped_column(Float, default=100.0)
    unit: Mapped[str] = mapped_column(String(20), default="gram")
    delivery_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    supplier: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cost_per_unit: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="ingredient"
    )
    inventory_logs: Mapped[list["InventoryLog"]] = relationship(
        "InventoryLog", back_populates="ingredient"
    )

    @property
    def is_low_stock(self) -> bool:
        """Check if ingredient is below minimum threshold"""
        return self.quantity_grams <= self.minimum_threshold

    def __repr__(self) -> str:
        return f"<Ingredient(name='{self.name}', quantity={self.quantity_grams}g)>"
