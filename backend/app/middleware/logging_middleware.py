from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from app.core.logging import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request
        logger.info(f"Request {request_id} started: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            
            # Log response
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"Request {request_id} completed: {response.status_code} - {process_time:.2f}ms"
            )
            
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time-MS"] = str(int(process_time))
            
            return response
            
        except Exception as e:
            logger.error(f"Request {request_id} failed: {str(e)}")
            raise