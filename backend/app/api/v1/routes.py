from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, sentiment, emotion, analytics, upload, voice, ocr, admin, websocket

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
api_router.include_router(emotion.router, prefix="/emotion", tags=["emotion"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
