from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SentinelMind AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str
    API_VERSION: str = "v1"
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    
    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    DATABASE_URL: str
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        
        # Check if we have PostgreSQL credentials
        user = values.get('POSTGRES_USER')
        password = values.get('POSTGRES_PASSWORD')
        db = values.get('POSTGRES_DB')
        
        if user and password and db:
            return f"postgresql+asyncpg://{user}:{password}@{values.get('POSTGRES_HOST', 'localhost')}:{values.get('POSTGRES_PORT', 5432)}/{db}"
        
        # Default to SQLite
        return "sqlite+aiosqlite:///./sentinelmind.db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8081"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # ML Settings
    SENTIMENT_MODEL_PATH: str = "./models/sentiment"
    EMOTION_MODEL_PATH: str = "./models/emotion"
    USE_GPU: bool = False
    BATCH_SIZE: int = 32
    MAX_SEQUENCE_LENGTH: int = 512
    MODEL_CACHE_SIZE: int = 1000
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = [".txt", ".csv", ".json", ".pdf", ".jpg", ".png"]
    UPLOAD_DIR: str = "./uploads"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    SENTRY_DSN: Optional[str] = None
    
    # External Services
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_CLOUD_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # This ignores extra fields like SMTP_*

settings = Settings()