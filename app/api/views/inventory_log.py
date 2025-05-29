from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database.config import get_general_session
from app.api.repositories.inventory_log import InventoryLogRepository
from app.api.schemas.inventory_log import InventoryLogCreate, InventoryLogResponse
from app.core.security import get_current_active_user
from app.api.models.user import User
from app.api.models.inventory_log import InventoryLog
from app.api.tasks.inventory_tasks import process_inventory_log
from app.api.websocket.connection_manager import manager
import json

router = APIRouter(prefix="/inventory-logs", tags=["InventoryLogs"])


@router.get("/", response_model=List[InventoryLogResponse])
async def get_inventory_logs(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = InventoryLogRepository(session)
    logs = await repo.get_all()
    return logs


@router.get("/{log_id}", response_model=InventoryLogResponse)
async def get_inventory_log(
    log_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = InventoryLogRepository(session)
    log = await repo.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory log not found")
    return log


@router.post("/", response_model=InventoryLogResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_log(
    log_create: InventoryLogCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    log = InventoryLog(**log_create.dict())
    created_log = await InventoryLogRepository(session).create(log)

    # Celery taskni chaqirish
    process_inventory_log.delay(created_log.id)

    # WebSocket orqali jonli xabar yuborish
    await manager.broadcast(json.dumps({
        "event": "inventory_update",
        "ingredient_id": created_log.ingredient_id,
        "new_quantity": created_log.new_quantity
    }))

    return created_log


# @router.post("/", response_model=InventoryLogResponse, status_code=status.HTTP_201_CREATED)
# async def create_inventory_log(
#     log_create: InventoryLogCreate,
#     current_user: User = Depends(get_current_active_user),
#     session: AsyncSession = Depends(get_general_session),
# ):
#     # Role tekshiruvi — masalan faqat admin va manager yozishi mumkin
#     if current_user.role not in ["admin", "manager"]:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
#
#     log = InventoryLog(**log_create.dict())
#     created_log = await InventoryLogRepository(session).create(log)
#     return created_log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_log(
    log_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = InventoryLogRepository(session)
    log = await repo.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory log not found")

    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await repo.delete(log)
    return None
