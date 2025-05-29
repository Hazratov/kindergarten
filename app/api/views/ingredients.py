from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.models import Ingredient
from app.core.database.config import get_general_session
from app.api.repositories.ingredient import IngredientRepository
from app.api.schemas.ingredient import (
    IngredientCreate,
    IngredientResponse,
    IngredientUpdate,
)
from app.core.security import get_current_active_user
from app.api.models.user import User

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.get("/", response_model=List[IngredientResponse])
async def get_ingredients(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = IngredientRepository(session)
    ingredients = await repo.get_all()
    return ingredients


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = IngredientRepository(session)
    ingredient = await repo.get_by_id(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    return ingredient


@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    ingredient_create: IngredientCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    # Masalan, faqat admin va manager ingredient yaratishi mumkin
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    repo = IngredientRepository(session)
    ingredient = Ingredient(**ingredient_create.dict())
    created = await repo.create(ingredient)
    return created


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: int,
    ingredient_update: IngredientUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = IngredientRepository(session)
    ingredient = await repo.get_by_id(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    update_data = ingredient_update.dict(exclude_unset=True)
    updated = await repo.update(ingredient, update_data)
    return updated


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = IngredientRepository(session)
    ingredient = await repo.get_by_id(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await repo.delete(ingredient)
    return None
