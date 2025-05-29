from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ChangeType(str, Enum):
    delivery = "delivery"
    consumption = "consumption"
    waste = "waste"
    adjustment = "adjustment"


class InventoryLogBase(BaseModel):
    ingredient_id: int
    change_amount: float  # + yoki - qiymat
    change_type: ChangeType
    reason: str
    reference_id: Optional[int] = None
    changed_by: int
    previous_quantity: float
    new_quantity: float


class InventoryLogCreate(InventoryLogBase):
    pass


class InventoryLogResponse(InventoryLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
