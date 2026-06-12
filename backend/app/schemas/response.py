from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    status: str = "success"
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    error: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class ErrorResponseModel(BaseModel):
    status: str = "error"
    error_type: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime = datetime.utcnow()