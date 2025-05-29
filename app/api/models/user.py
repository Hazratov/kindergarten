from enum import Enum as PyEnum  # Python standarti
from sqlalchemy import String, Boolean
from sqlalchemy.types import Enum as PgEnum  # SQLAlchemy uchun enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import Base, TimestampMixin


class UserRole(PyEnum):
    admin = "admin"
    cook = "cook"  # Oshpaz
    manager = "manager"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    created_recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", back_populates="created_by_user"
    )
    meal_logs: Mapped[list["MealLog"]] = relationship(
        "MealLog", back_populates="served_by_user"
    )
    inventory_logs: Mapped[list["InventoryLog"]] = relationship(
        "InventoryLog", back_populates="changed_by_user"
    )
    monthly_reports: Mapped[list["MonthlyReport"]] = relationship(
        "MonthlyReport", back_populates="generated_by_user"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', role='{self.role}')>"