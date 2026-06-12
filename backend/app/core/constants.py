# API Constants
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Sentiment Labels
SENTIMENT_LABELS = {
    0: "negative",
    1: "neutral", 
    2: "positive"
}

# Emotion Labels
EMOTION_LABELS = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

# Language Codes
SUPPORTED_LANGUAGES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "tr": "Turkish",
    "pl": "Polish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "th": "Thai",
    "el": "Greek",
    "he": "Hebrew",
    "fa": "Persian"
}

# Model Configurations
MODEL_CONFIGS = {
    "sentiment": {
        "model_name": "cardiffnlp/twitter-xlm-roberta-base-sentiment",
        "max_length": 512,
        "batch_size": 32,
        "num_labels": 3
    },
    "emotion": {
        "model_name": "bhadresh-savani/distilbert-base-uncased-emotion",
        "max_length": 512,
        "batch_size": 32,
        "num_labels": 6
    },
    "toxicity": {
        "model_name": "unitary/toxic-bert",
        "max_length": 512,
        "batch_size": 32
    },
    "embedding": {
        "model_name": "paraphrase-multilingual-MiniLM-L12-v2",
        "embedding_dim": 384
    }
}

# Cache Settings
CACHE_TTL = {
    "sentiment": 3600,  # 1 hour
    "emotion": 3600,
    "toxicity": 3600,
    "embedding": 86400,  # 24 hours
    "analytics": 300,  # 5 minutes
    "user_stats": 600  # 10 minutes
}

# Rate Limits
RATE_LIMITS = {
    "free": {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "requests_per_day": 500,
        "batch_size": 10,
        "file_size_mb": 5
    },
    "premium": {
        "requests_per_minute": 100,
        "requests_per_hour": 2000,
        "requests_per_day": 10000,
        "batch_size": 100,
        "file_size_mb": 50
    },
    "enterprise": {
        "requests_per_minute": 1000,
        "requests_per_hour": 50000,
        "requests_per_day": 100000,
        "batch_size": 1000,
        "file_size_mb": 200
    }
}

# File Upload Settings
ALLOWED_MIME_TYPES = {
    "text": ["text/plain", "text/csv", "application/json"],
    "image": ["image/jpeg", "image/png", "image/tiff", "image/bmp"],
    "document": ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    "audio": ["audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a"]
}

# WebSocket Events
WEBSOCKET_EVENTS = {
    "CONNECT": "connection_established",
    "DISCONNECT": "connection_closed",
    "ANALYSIS_START": "analysis_started",
    "ANALYSIS_COMPLETE": "analysis_complete",
    "ANALYSIS_ERROR": "analysis_error",
    "STREAM_START": "stream_started",
    "STREAM_DATA": "stream_data",
    "STREAM_END": "stream_ended"
}

# Analytics Intervals
ANALYTICS_INTERVALS = ["hour", "day", "week", "month", "year"]

# Notification Types
NOTIFICATION_TYPES = {
    "EMAIL": "email",
    "WEBHOOK": "webhook",
    "PUSH": "push_notification",
    "SMS": "sms"
}

# Task Status
TASK_STATUS = {
    "PENDING": "pending",
    "PROCESSING": "processing",
    "COMPLETED": "completed",
    "FAILED": "failed",
    "CANCELLED": "cancelled"
}