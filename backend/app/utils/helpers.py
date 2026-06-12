import random
import string
from datetime import datetime, timedelta
from typing import Optional

def generate_random_string(length: int = 32) -> str:
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_otp(length: int = 6) -> str:
    """Generate OTP code"""
    return ''.join(random.choices(string.digits, k=length))

def format_timestamp(timestamp: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format timestamp"""
    return timestamp.strftime(format)

def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """Parse timestamp string"""
    try:
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except:
        return None

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safely divide two numbers"""
    try:
        return a / b if b != 0 else default
    except:
        return default