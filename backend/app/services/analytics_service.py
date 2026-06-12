from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

from app.models.analysis import Analysis
from app.models.user import User
from app.core.redis_client import redis_client
from app.core.config import settings
import json

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_dashboard_stats(self, user_id: int, days: int = 30) -> Dict:
        """Get comprehensive dashboard statistics"""
        cache_key = f"dashboard_stats:{user_id}:{days}"
        
        # Try cache first
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total analyses
        total_query = select(func.count(Analysis.id)).where(
            Analysis.user_id == user_id,
            Analysis.created_at >= start_date
        )
        total_analyses = await self.db.execute(total_query)
        total = total_analyses.scalar() or 0
        
        # Sentiment distribution
        sentiment_dist = await self.db.execute(
            select(Analysis.sentiment_label, func.count(Analysis.id))
            .where(Analysis.user_id == user_id, Analysis.created_at >= start_date)
            .group_by(Analysis.sentiment_label)
        )
        
        # Top emotions
        emotion_counts = {}
        emotion_query = await self.db.execute(
            select(Analysis.dominant_emotion, func.count(Analysis.id))
            .where(Analysis.user_id == user_id, Analysis.created_at >= start_date)
            .group_by(Analysis.dominant_emotion)
        )
        
        for emotion, count in emotion_query:
            if emotion:
                emotion_counts[emotion] = count
        
        # Language distribution
        lang_dist = await self.db.execute(
            select(Analysis.language, func.count(Analysis.id))
            .where(Analysis.user_id == user_id, Analysis.created_at >= start_date)
            .group_by(Analysis.language)
            .limit(5)
        )
        
        # Average confidence
        avg_confidence = await self.db.execute(
            select(func.avg(Analysis.sentiment_confidence))
            .where(Analysis.user_id == user_id, Analysis.created_at >= start_date)
        )
        
        # Get user info for API limits
        user = await self.db.get(User, user_id)
        
        stats = {
            "total_analyses": total,
            "average_sentiment_score": await self._calculate_avg_sentiment_score(user_id, start_date),
            "sentiment_distribution": dict(sentiment_dist.all()),
            "top_emotions": sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "language_distribution": dict(lang_dist.all()),
            "average_confidence": float(avg_confidence.scalar() or 0),
            "daily_active_users": await self._get_daily_active_users(),
            "api_calls_remaining": user.api_calls_limit - user.api_calls_used if user else 0,
            "premium_features_used": await self._count_premium_features(user_id, start_date)
        }
        
        # Cache for 10 minutes
        await redis_client.setex(cache_key, 600, json.dumps(stats))
        
        return stats
    
    async def get_sentiment_trends(self, user_id: int, start_date: datetime, 
                                   end_date: datetime, interval: str = "day") -> Dict:
        """Get sentiment trends over time"""
        # Generate date series based on interval
        dates = pd.date_range(start=start_date, end=end_date, freq=interval[0].upper())
        
        trends = []
        for date in dates:
            next_date = date + timedelta(days=1 if interval == "day" else 7)
            
            # Get sentiment distribution for period
            result = await self.db.execute(
                select(
                    func.sum(case((Analysis.sentiment_label == "positive", 1), else_=0)).label("positive"),
                    func.sum(case((Analysis.sentiment_label == "negative", 1), else_=0)).label("negative"),
                    func.sum(case((Analysis.sentiment_label == "neutral", 1), else_=0)).label("neutral"),
                    func.count(Analysis.id).label("total")
                )
                .where(
                    Analysis.user_id == user_id,
                    Analysis.created_at >= date,
                    Analysis.created_at <= next_date
                )
            )
            
            row = result.one()
            total = row.total or 1
            
            trends.append({
                "date": date.strftime("%Y-%m-%d"),
                "positive": (row.positive or 0) / total,
                "negative": (row.negative or 0) / total,
                "neutral": (row.neutral or 0) / total
            })
        
        # Calculate overall trend
        if len(trends) >= 2:
            sentiment_values = [t["positive"] - t["negative"] for t in trends]
            slope = np.polyfit(range(len(sentiment_values)), sentiment_values, 1)[0]
            overall_trend = "improving" if slope > 0.01 else "declining" if slope < -0.01 else "stable"
            volatility = float(np.std(sentiment_values))
        else:
            overall_trend = "stable"
            volatility = 0.0
        
        return {
            "trends": trends,
            "overall_trend": overall_trend,
            "volatility": volatility,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "interval": interval
        }
    
    async def get_emotion_distribution(self, user_id: int, days: int = 30) -> Dict:
        """Get emotion distribution analytics"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        result = await self.db.execute(
            select(Analysis.dominant_emotion, func.count(Analysis.id))
            .where(
                Analysis.user_id == user_id,
                Analysis.created_at >= start_date,
                Analysis.dominant_emotion.isnot(None)
            )
            .group_by(Analysis.dominant_emotion)
        )
        
        emotions = dict(result.all())
        total = sum(emotions.values()) or 1
        
        return {
            "distribution": {k: v/total for k, v in emotions.items()},
            "counts": emotions,
            "total_analyses": total,
            "period_days": days
        }
    
    async def get_top_keywords(self, user_id: int, limit: int = 20, days: int = 30) -> List[str]:
        """Get most frequent keywords from analyses"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # This would use PostgreSQL full-text search or a keywords column
        # Simplified version - would need proper implementation
        result = await self.db.execute(
            text("""
                SELECT unnest(string_to_array(cleaned_text, ' ')) as word,
                       COUNT(*) as frequency
                FROM analyses
                WHERE user_id = :user_id
                  AND created_at >= :start_date
                  AND cleaned_text IS NOT NULL
                GROUP BY word
                ORDER BY frequency DESC
                LIMIT :limit
            """),
            {"user_id": user_id, "start_date": start_date, "limit": limit}
        )
        
        keywords = [row.word for row in result if len(row.word) > 3]
        return keywords
    
    async def get_performance_metrics(self, hours: int = 24) -> Dict:
        """Get system performance metrics"""
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Average latency
        latency = await self.db.execute(
            select(func.avg(Analysis.processing_time_ms))
            .where(Analysis.created_at >= start_time)
        )
        
        # Percentiles - would require more complex query
        p95_result = await self.db.execute(
            text("""
                SELECT percentile_cont(0.95) WITHIN GROUP (ORDER BY processing_time_ms)
                FROM analyses
                WHERE created_at >= :start_time
            """),
            {"start_time": start_time}
        )
        
        # Requests per second
        total_requests = await self.db.execute(
            select(func.count(Analysis.id))
            .where(Analysis.created_at >= start_time)
        )
        rps = total_requests.scalar() / (hours * 3600) if hours > 0 else 0
        
        # Error rate
        # Would need error logging table
        
        return {
            "average_latency_ms": float(latency.scalar() or 0),
            "p95_latency_ms": float(p95_result.scalar() or 0),
            "p99_latency_ms": 0,  # Would calculate similarly
            "requests_per_second": round(rps, 2),
            "error_rate": 0.0,  # Would calculate from error logs
            "model_throughput": int(rps * 60),  # Requests per minute
            "gpu_utilization": None  # Would get from monitoring
        }
    
    async def export_data(self, user_id: int, request: Dict) -> str:
        """Export analytics data as CSV/JSON"""
        start_date = request.get("start_date")
        end_date = request.get("end_date")
        export_format = request.get("format", "json")
        
        # Query data
        query = select(Analysis).where(
            Analysis.user_id == user_id,
            Analysis.created_at >= start_date,
            Analysis.created_at <= end_date
        )
        
        result = await self.db.execute(query)
        analyses = result.scalars().all()
        
        # Convert to dict
        data = [a.to_dict() for a in analyses]
        
        if export_format == "csv":
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            # Would save to file and return URL
            return f"/exports/analytics_{user_id}_{datetime.utcnow().timestamp()}.csv"
        else:
            # Return JSON
            return json.dumps(data, default=str)
    
    async def get_realtime_stats(self, user_id: int) -> Dict:
        """Get real-time analytics (last hour)"""
        last_hour = datetime.utcnow() - timedelta(hours=1)
        
        # Recent analyses
        recent = await self.db.execute(
            select(Analysis)
            .where(Analysis.user_id == user_id, Analysis.created_at >= last_hour)
            .order_by(Analysis.created_at.desc())
            .limit(10)
        )
        
        recent_analyses = [a.to_dict() for a in recent.scalars().all()]
        
        # Current sentiment trend (last 60 minutes, minute by minute)
        minute_stats = []
        for i in range(60):
            minute_start = last_hour + timedelta(minutes=i)
            minute_end = minute_start + timedelta(minutes=1)
            
            minute_result = await self.db.execute(
                select(func.avg(case((Analysis.sentiment_label == "positive", 1),
                                    (Analysis.sentiment_label == "negative", -1),
                                    else_=0)))
                .where(
                    Analysis.user_id == user_id,
                    Analysis.created_at >= minute_start,
                    Analysis.created_at <= minute_end
                )
            )
            
            score = minute_result.scalar()
            if score is not None:
                minute_stats.append({
                    "minute": i,
                    "score": float(score)
                })
        
        return {
            "recent_analyses": recent_analyses,
            "last_hour_sentiment": minute_stats,
            "current_rate": len(recent_analyses) / 60,  # analyses per minute
            "websocket_connected": False  # Would check WebSocket status
        }
    
    async def _calculate_avg_sentiment_score(self, user_id: int, start_date: datetime) -> float:
        """Calculate average sentiment score (-1 to 1)"""
        result = await self.db.execute(
            select(func.avg(
                case(
                    (Analysis.sentiment_label == "positive", 1),
                    (Analysis.sentiment_label == "negative", -1),
                    else_=0
                )
            ))
            .where(Analysis.user_id == user_id, Analysis.created_at >= start_date)
        )
        return float(result.scalar() or 0)
    
    async def _get_daily_active_users(self) -> int:
        """Get number of active users in last 24 hours"""
        last_day = datetime.utcnow() - timedelta(days=1)
        result = await self.db.execute(
            select(func.count(func.distinct(Analysis.user_id)))
            .where(Analysis.created_at >= last_day)
        )
        return result.scalar() or 0
    
    async def _count_premium_features(self, user_id: int, start_date: datetime) -> int:
        """Count usage of premium features"""
        # Count analyses with emotions, toxicity, or batch processing
        result = await self.db.execute(
            select(func.count(Analysis.id))
            .where(
                Analysis.user_id == user_id,
                Analysis.created_at >= start_date,
                Analysis.emotions.isnot(None)
            )
        )
        return result.scalar() or 0