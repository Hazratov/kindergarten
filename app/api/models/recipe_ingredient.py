from sqlalchemy import ForeignKey, Float, Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    required_grams: Mapped[float] = mapped_column(Float, nullable=False)
    is_optional: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    recipe: Mapped["Recipe"] = relationship(
        "Recipe", back_populates="recipe_ingredients"
    )
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="recipe_ingredients"
    )

    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint('recipe_id', 'ingredient_id', name='_recipe_ingredient_uc'),
    )

    def __repr__(self) -> str:
        return f"<RecipeIngredient(recipe_id={self.recipe_id}, ingredient_id={self.ingredient_id}, grams={self.required_grams})>"
