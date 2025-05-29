from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from sqlalchemy.orm import selectinload

from app.core.database.config import get_general_session
from app.api.repositories.recipe import RecipeRepository
from app.api.schemas.recipe import RecipeCreate, RecipeResponse, RecipeUpdate
from app.core.security import get_current_active_user
from app.api.models.user import User
from app.api.models.recipe import Recipe
from app.api.models.recipe_ingredient import RecipeIngredient

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = RecipeRepository(session)
    # Eager loading all recipes with their ingredients
    recipes = await repo.get_all()
    return recipes


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = RecipeRepository(session)
    recipe = await repo.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_create: RecipeCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    recipe = Recipe(
        name=recipe_create.name,
        description=recipe_create.description,
        preparation_time=recipe_create.preparation_time,
        cooking_time=recipe_create.cooking_time,
        servings_count=recipe_create.servings_count,
        difficulty_level=recipe_create.difficulty_level.value,  # .value ishlatilmoqda
        instructions=recipe_create.instructions,
        is_active=recipe_create.is_active,
        created_by=current_user.id,
    )

    ingredients = []
    for ing_data in recipe_create.recipe_ingredients:
        ingredients.append(
            RecipeIngredient(
                ingredient_id=ing_data.ingredient_id,
                required_grams=ing_data.required_grams,
                is_optional=ing_data.is_optional or False,
                notes=ing_data.notes,
            )
        )
    recipe.recipe_ingredients = ingredients

    repo = RecipeRepository(session)
    created_recipe = await repo.create(recipe)
    return created_recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = RecipeRepository(session)
    recipe = await repo.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    update_data = recipe_update.dict(exclude_unset=True)

    if "difficulty_level" in update_data:
        update_data["difficulty_level"] = update_data["difficulty_level"].value

    if "recipe_ingredients" in update_data:
        recipe.recipe_ingredients.clear()
        new_ingredients = []
        for ing_data in update_data["recipe_ingredients"]:
            new_ingredients.append(
                RecipeIngredient(
                    ingredient_id=ing_data.ingredient_id,
                    required_grams=ing_data.required_grams,
                    is_optional=ing_data.is_optional or False,
                    notes=ing_data.notes,
                )
            )
        recipe.recipe_ingredients = new_ingredients
        update_data.pop("recipe_ingredients")

    updated_recipe = await repo.update(recipe, update_data)
    return updated_recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = RecipeRepository(session)
    recipe = await repo.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await repo.delete(recipe)
    return None
