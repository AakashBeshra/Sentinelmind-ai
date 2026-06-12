from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int

class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
    timestamp: datetime