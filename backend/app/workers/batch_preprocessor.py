from celery import Celery
from typing import List, Dict
import asyncio

from app.core.config import settings
from app.services.sentiment_service import SentimentService
from app.core.logging import logger

# Initialize Celery
celery_app = Celery(
    'sentinelmind',
    broker=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
    backend=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
)

@celery_app.task(bind=True, name='batch_sentiment_analysis')
def batch_sentiment_analysis(self, texts: List[str], options: Dict = None):
    """Batch sentiment analysis task"""
    try:
        # Update task state        self.update_state(state='PROCESSING', meta={'current': 0, 'total': len(texts)})
        
        results = []
        for i, text in enumerate(texts):
            # Run analysis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(SentimentService.analyze(text, **(options or {})))
            loop.close()
            
            results.append(result)
            
            # Update progress
            self.update_state(state='PROCESSING', meta={'current': i + 1, 'total': len(texts)})
        
        return {
            'status': 'completed',
            'total': len(results),
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        return {
            'status': 'failed',
            'error': str(e)
        }

@celery_app.task(name='cleanup_expired_data')
def cleanup_expired_data():
    """Clean up expired data periodically"""
    # Implementation for data cleanup
    pass