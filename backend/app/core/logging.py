import logging
import sys
from logging.handlers import RotatingFileHandler
from loguru import logger as loguru_logger
import json
from datetime import datetime

from app.core.config import settings

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

def setup_logging():
    """Configure application logging"""
    # Remove default handlers
    loguru_logger.remove()
    
    # Console logging
    loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True
    )
    
    # File logging (JSON format for production)
    if not settings.DEBUG:
        loguru_logger.add(
            "logs/app.log",
            rotation="500 MB",
            retention="30 days",
            compression="gz",
            format="{time} | {level} | {name} | {message}",
            level="INFO",
            serialize=True
        )
        
        # Error file
        loguru_logger.add(
            "logs/error.log",
            rotation="100 MB",
            retention="90 days",
            level="ERROR",
            format="{time} | {level} | {name} | {message}",
            serialize=True
        )
    
    # Configure standard logging for third-party libraries
    logging.basicConfig(level=logging.WARNING)
    
    # Reduce verbosity of some loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    loguru_logger.info(f"Logging configured - Environment: {settings.ENVIRONMENT}")
    
    return loguru_logger

# Export logger
logger = setup_logging()