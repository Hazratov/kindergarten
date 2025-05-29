from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database.config import get_general_session
from app.api.repositories.meal_log import MealLogRepository
from app.api.schemas.meal import MealLogCreate, MealLogResponse
from app.core.security import get_current_active_user
from app.api.models.user import User
from app.api.models.meal_log import MealLog

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.get("/", response_model=List[MealLogResponse])
async def get_meals(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = MealLogRepository(session)
    meals = await repo.get_all()
    return meals


@router.get("/{meal_id}", response_model=MealLogResponse)
async def get_meal(
    meal_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = MealLogRepository(session)
    meal = await repo.get_by_id(meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal log not found")
    return meal


@router.post("/", response_model=MealLogResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal_create: MealLogCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    # Masalan, faqat admin, manager va oshpazlar yozishi mumkin
    if current_user.role not in ["admin", "manager", "cook"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    meal = MealLog(**meal_create.dict())
    created_meal = await MealLogRepository(session).create(meal)
    return created_meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = MealLogRepository(session)
    meal = await repo.get_by_id(meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal log not found")

    # Faqat admin yoki manager o‘chira oladi
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await repo.delete(meal)
    return None
