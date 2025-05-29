from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DifficultyLevel(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    required_grams: float
    is_optional: Optional[bool] = False
    notes: Optional[str] = None


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    id: int

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    preparation_time: int  # minutes
    cooking_time: int  # minutes
    servings_count: int
    difficulty_level: DifficultyLevel
    instructions: Optional[str] = None
    is_active: Optional[bool] = True


class RecipeCreate(RecipeBase):
    recipe_ingredients: List[RecipeIngredientCreate]


class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    preparation_time: Optional[int] = None
    cooking_time: Optional[int] = None
    servings_count: Optional[int] = None
    difficulty_level: Optional[DifficultyLevel] = None
    instructions: Optional[str] = None
    is_active: Optional[bool] = None
    recipe_ingredients: Optional[List[RecipeIngredientCreate]] = None


class RecipeResponse(RecipeBase):
    id: int
    recipe_ingredients: List[RecipeIngredientResponse]

    class Config:
        orm_mode = True
