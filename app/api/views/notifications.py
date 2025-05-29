from fastapi import APIRouter, Depends, HTTPException, WebSocket, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database.config import get_general_session
from app.api.repositories.notification import NotificationRepository
from app.api.schemas.notification import NotificationResponse
from app.core.security import get_current_active_user
from app.api.models.user import User
from app.api.websocket.connection_manager import manager

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_general_session),
):
    repo = NotificationRepository(session)
    notifications = await repo.get_all_for_user(current_user.id)
    return notifications


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Bu yerda websocketdan kelgan xabarni ishlash mumkin
            await manager.broadcast(f"Broadcast message: {data}")
    except Exception:
        manager.disconnect(websocket)
