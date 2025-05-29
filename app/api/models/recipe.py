from enum import Enum as PyEnum
from sqlalchemy import String, Text, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base, TimestampMixin


class DifficultyLevel(PyEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Recipe(Base, TimestampMixin):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    preparation_time: Mapped[int] = mapped_column(Integer, default=0)  # minutes
    cooking_time: Mapped[int] = mapped_column(Integer, default=0)  # minutes
    servings_count: Mapped[int] = mapped_column(Integer, default=1)  # portions
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel, name="difficultylevel"), default=DifficultyLevel.easy
    )
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    created_by_user: Mapped["User"] = relationship(
        "User", back_populates="created_recipes"
    )
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan"
    )
    meal_logs: Mapped[list["MealLog"]] = relationship(
        "MealLog", back_populates="recipe"
    )

    @property
    def total_time(self) -> int:
        """Total preparation + cooking time"""
        return self.preparation_time + self.cooking_time

    def __repr__(self) -> str:
        return f"<Recipe(name='{self.name}', servings={self.servings_count})>"