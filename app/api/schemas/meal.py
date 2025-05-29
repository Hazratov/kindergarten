from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class MealStatus(str, Enum):
    completed = "completed"
    cancelled = "cancelled"


class MealLogBase(BaseModel):
    recipe_id: int
    served_by: int
    portions_served: int
    served_at: datetime
    children_count: Optional[int] = None
    notes: Optional[str] = None
    status: MealStatus = MealStatus.completed


class MealLogCreate(MealLogBase):
    pass


class MealLogResponse(MealLogBase):
    id: int

    class Config:
        orm_mode = True
