from fastapi import APIRouter, WebSocket
router = APIRouter()
@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"message": "Connected to WebSocket"})
    await websocket.close()
