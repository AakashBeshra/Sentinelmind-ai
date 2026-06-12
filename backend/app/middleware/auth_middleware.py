from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        public_paths = ['/health', '/docs', '/redoc', '/openapi.json', '/api/v1/auth']
        
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Check for token
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing authorization header")
        
        try:
            token = auth_header.replace('Bearer ', '')
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            request.state.user_id = payload.get('sub')
            request.state.user_role = payload.get('role')
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return await call_next(request)