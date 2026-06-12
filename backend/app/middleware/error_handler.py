from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
from app.core.logging import logger

async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(e) if request.app.debug else "An unexpected error occurred"
            }
        )