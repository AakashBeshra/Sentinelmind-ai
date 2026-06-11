import pytest
from unittest.mock import AsyncMock, patch

from app.services.sentiment_service import SentimentService
from app.ml.model_manager import ModelManager


pytestmark = pytest.mark.asyncio


async def test_analyze_sentiment():
    """Test sentiment analysis service"""
    with patch.object(ModelManager, 'predict_sentiment', AsyncMock(return_value={
        "sentiment": "positive",
        "confidence": 0.95,
        "probabilities": {"positive": 0.95, "neutral": 0.03, "negative": 0.02}
    })):
        with patch.object(ModelManager, 'predict_emotions', AsyncMock(return_value={
            "dominant_emotion": "joy",
            "all_emotions": {"joy": 0.8, "sadness": 0.1}
        })):
            result = await SentimentService.analyze(
                "I love this product!",
                include_emotions=True
            )
            
            assert result["sentiment"] == "positive"
            assert result["confidence"] > 0
            assert "probabilities" in result
            assert "emotions" in result


async def test_analyze_without_emotions():
    """Test sentiment analysis without emotions"""
    with patch.object(ModelManager, 'predict_sentiment', AsyncMock(return_value={
        "sentiment": "positive",
        "confidence": 0.95,
        "probabilities": {"positive": 0.95, "neutral": 0.03, "negative": 0.02}
    })):
        result = await SentimentService.analyze(
            "Good product",
            include_emotions=False
        )
        
        assert "emotions" not in result


async def test_language_detection():
    """Test automatic language detection"""
    with patch.object(ModelManager, 'predict_sentiment', AsyncMock(return_value={
        "sentiment": "positive",
        "confidence": 0.9,
        "probabilities": {"positive": 0.9, "neutral": 0.1, "negative": 0.0}
    })):
        result = await SentimentService.analyze(
            "Me encanta este producto",
            language="auto"
        )
        
        assert result["language"] is not None


async def test_batch_analysis():
    """Test batch sentiment analysis"""
    texts = ["Great!", "Terrible!", "Okay"]
    
    with patch.object(SentimentService, 'analyze', AsyncMock(side_effect=[
        {"sentiment": "positive", "confidence": 0.9},
        {"sentiment": "negative", "confidence": 0.85},
        {"sentiment": "neutral", "confidence": 0.7}
    ])):
        results = await SentimentService.batch_analyze(texts)
        
        assert len(results) == 3
        assert results[0]["sentiment"] == "positive"
        assert results[1]["sentiment"] == "negative"


async def test_analysis_with_toxicity():
    """Test sentiment analysis with toxicity detection"""
    with patch.object(ModelManager, 'predict_sentiment', AsyncMock(return_value={
        "sentiment": "negative",
        "confidence": 0.9,
        "probabilities": {"positive": 0.05, "neutral": 0.05, "negative": 0.9}
    })):
        with patch.object(ModelManager, 'detect_toxicity', AsyncMock(return_value={
            "is_toxic": True,
            "confidence": 0.88
        })):
            result = await SentimentService.analyze(
                "This is a terrible product",
                include_toxicity=True
            )
            
            assert "toxicity" in result
            assert result["toxicity"]["is_toxic"] is True