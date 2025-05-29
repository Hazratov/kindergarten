from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MonthlyReportBase(BaseModel):
    month: int  # 1-12
    year: int
    total_portions_served: Optional[int] = 0
    total_possible_portions: Optional[int] = 0
    wastage_percentage: Optional[float] = 0.0
    total_ingredients_used: Optional[float] = 0.0
    total_cost: Optional[float] = None
    efficiency_score: Optional[float] = 0.0


class MonthlyReportResponse(MonthlyReportBase):
    id: int
    generated_at: datetime
    generated_by: int

    class Config:
        orm_mode = True
