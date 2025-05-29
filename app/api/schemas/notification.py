from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    info = "info"
    warning = "warning"
    alert = "alert"
    success = "success"


class NotificationPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    type: NotificationType = NotificationType.info
    priority: NotificationPriority = NotificationPriority.medium
    is_read: bool = False
    is_system_generated: bool = True
    related_model: Optional[str] = None
    related_id: Optional[int] = None
    expires_at: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
