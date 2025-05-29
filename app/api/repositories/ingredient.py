from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.models.ingredient import Ingredient
from typing import List, Optional


class IngredientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Ingredient]:
        result = await self.session.execute(select(Ingredient))
        return result.scalars().all()

    async def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        result = await self.session.execute(
            select(Ingredient).where(Ingredient.id == ingredient_id)
        )
        return result.scalar_one_or_none()

    async def create(self, ingredient: Ingredient) -> Ingredient:
        self.session.add(ingredient)
        await self.session.commit()
        await self.session.refresh(ingredient)
        return ingredient

    async def update(self, ingredient: Ingredient, data: dict) -> Ingredient:
        for key, value in data.items():
            setattr(ingredient, key, value)
        self.session.add(ingredient)
        await self.session.commit()
        await self.session.refresh(ingredient)
        return ingredient

    async def delete(self, ingredient: Ingredient) -> None:
        await self.session.delete(ingredient)
        await self.session.commit()
