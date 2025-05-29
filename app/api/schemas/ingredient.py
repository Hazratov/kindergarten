from pydantic import BaseModel
from typing import Optional


class IngredientBase(BaseModel):
    name: str
    quantity_grams: float  # grammda umumiy miqdor


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    quantity_grams: Optional[float] = None


class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True
