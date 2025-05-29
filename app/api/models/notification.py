from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, Boolean, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.core.models.base import Base


class NotificationType(PyEnum):
    info = "info"
    warning = "warning"
    alert = "alert"
    success = "success"


class NotificationPriority(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType), default=NotificationType.info
    )
    priority: Mapped[NotificationPriority] = mapped_column(
        Enum(NotificationPriority), default=NotificationPriority.medium
    )
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    is_system_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    related_model: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    related_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    @property
    def is_expired(self) -> bool:
        """Check if notification has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def __repr__(self) -> str:
        return f"<Notification(title='{self.title}', type='{self.type.value}', priority='{self.priority.value}')>"