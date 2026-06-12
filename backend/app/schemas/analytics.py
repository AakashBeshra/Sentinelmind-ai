from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class DashboardStats(BaseModel):
    total_analyses: int
    average_sentiment_score: float
    sentiment_distribution: Dict[str, int]
    top_emotions: List[Dict[str, float]]
    daily_active_users: int
    api_calls_remaining: int
    premium_features_used: int

class SentimentTrend(BaseModel):
    date: str
    positive: float
    negative: float
    neutral: float

class SentimentTrends(BaseModel):
    trends: List[SentimentTrend]
    overall_trend: str  # improving, stable, declining
    volatility: float

class UserAnalytics(BaseModel):
    user_id: int
    total_analyses: int
    sentiment_history: List[Dict]
    preferred_languages: List[str]
    average_confidence: float
    average_processing_time: float

class PerformanceMetrics(BaseModel):
    average_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    requests_per_second: float
    error_rate: float
    model_throughput: int
    gpu_utilization: Optional[float]

class ExportDataRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    format: str  # csv, json
    include_metadata: bool = True
    include_raw_text: bool = False