from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.api.models.recipe import Recipe
from app.api.models.recipe_ingredient import RecipeIngredient


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Recipe]:
        result = await self.session.execute(
            select(Recipe).options(selectinload(Recipe.recipe_ingredients))
        )
        return result.scalars().all()

    async def get_by_id(self, recipe_id: int) -> Recipe | None:
        result = await self.session.execute(
            select(Recipe)
            .where(Recipe.id == recipe_id)
            .options(selectinload(Recipe.recipe_ingredients))
        )
        return result.scalar_one_or_none()

    async def create(self, recipe: Recipe) -> Recipe:
        self.session.add(recipe)
        await self.session.commit()
        await self.session.refresh(recipe)
        return recipe

    async def update(self, recipe: Recipe, data: dict) -> Recipe:
        for key, value in data.items():
            setattr(recipe, key, value)
        self.session.add(recipe)
        await self.session.commit()
        await self.session.refresh(recipe)
        return recipe

    async def delete(self, recipe: Recipe) -> None:
        await self.session.delete(recipe)
        await self.session.commit()
