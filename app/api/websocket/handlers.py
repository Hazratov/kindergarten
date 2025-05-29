from fastapi import WebSocket
from app.api.websocket.connection_manager import manager
import json

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Agar clientdan ma’lumot kelsa, uni qayta ishlash mumkin
            # Hozircha oddiy broadcast qilamiz
            await manager.broadcast(f"Message from client: {data}")
    except Exception:
        manager.disconnect(websocket)
