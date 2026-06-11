import pytest
from unittest.mock import AsyncMock, Mock, patch

from app.ml.model_manager import ModelManager
from app.ml.inference_engine import InferenceEngine, InferenceRequest


pytestmark = pytest.mark.asyncio


async def test_model_manager_sentiment():
    """Test sentiment prediction"""
    with patch.object(ModelManager, '_models', {'sentiment': Mock()}):
        with patch.object(ModelManager, '_tokenizers', {'sentiment': Mock()}):
            with patch('app.ml.model_manager.redis_client') as mock_redis:
                mock_redis.get = AsyncMock(return_value=None)
                
                result = await ModelManager.predict_sentiment("I love this!")
                
                assert "sentiment" in result
                assert "confidence" in result
                assert "probabilities" in result


async def test_model_manager_emotion():
    """Test emotion prediction"""
    with patch.object(ModelManager, '_models', {'emotion': Mock()}):
        with patch.object(ModelManager, '_tokenizers', {'emotion': Mock()}):
            with patch('app.ml.model_manager.redis_client') as mock_redis:
                mock_redis.get = AsyncMock(return_value=None)
                
                result = await ModelManager.predict_emotions("I feel great!")
                
                assert "dominant_emotion" in result
                assert "all_emotions" in result


async def test_inference_engine():
    """Test inference engine batch processing"""
    engine = InferenceEngine(Mock(), batch_size=2)
    engine.is_running = False
    
    request = InferenceRequest(
        text="Test text",
        task="sentiment",
        request_id="123",
        timestamp=0
    )
    
    with patch.object(engine, '_process_batch', AsyncMock()):
        result = await engine.predict(request)
        # Should handle gracefully


async def test_batch_prediction():
    """Test batch prediction"""
    texts = ["Good", "Bad", "Okay"]
    
    with patch.object(ModelManager, 'batch_predict', AsyncMock(return_value=[
        {"sentiment": "positive"},
        {"sentiment": "negative"},
        {"sentiment": "neutral"}
    ])):
        results = await ModelManager.batch_predict(texts, "sentiment")
        assert len(results) == 3


async def test_caching():
    """Test prediction caching"""
    with patch('app.ml.model_manager.redis_client') as mock_redis:
        mock_redis.get = AsyncMock(return_value=None)
        mock_redis.setex = AsyncMock()
        
        result1 = await ModelManager.predict_sentiment("Same text")
        result2 = await ModelManager.predict_sentiment("Same text")
        
        # Should use cache for second call
        assert mock_redis.get.call_count <= 2