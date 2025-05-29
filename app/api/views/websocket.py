from fastapi import APIRouter, WebSocket, Depends, status
from app.core.security import get_current_active_user

from app.api.websocket.handlers import websocket_endpoint

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/inventory-updates")
async def inventory_updates_ws(
    websocket: WebSocket,
    current_user=Depends(get_current_active_user)
):

    await websocket_endpoint(websocket)
