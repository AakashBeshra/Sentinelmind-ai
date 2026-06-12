from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional

class SentinelMindException(Exception):
    """Base exception for SentinelMind AI"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class NotFoundError(SentinelMindException):
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(
            message=f"{entity} with id {entity_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class UnauthorizedError(SentinelMindException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class ForbiddenError(SentinelMindException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )

class ValidationError(SentinelMindException):
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )

class RateLimitError(SentinelMindException):
    def __init__(self, limit: int, window: int):
        super().__init__(
            message=f"Rate limit exceeded. Maximum {limit} requests per {window} seconds",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

class ModelNotFoundError(SentinelMindException):
    def __init__(self, model_name: str):
        super().__init__(
            message=f"ML model '{model_name}' not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class QuotaExceededError(SentinelMindException):
    def __init__(self, quota_type: str, limit: int):
        super().__init__(
            message=f"{quota_type} quota exceeded. Limit: {limit}",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

def register_exception_handlers(app):
    """Register exception handlers for FastAPI app"""
    
    @app.exception_handler(SentinelMindException)
    async def sentinelmind_exception_handler(
        request: Request,
        exc: SentinelMindException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred"
            }
        )