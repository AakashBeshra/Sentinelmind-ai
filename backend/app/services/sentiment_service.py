from app.ml.model_manager import ModelManager
from app.nlp.preprocessor import TextPreprocessor
from app.core.redis_client import redis_client
from app.models.analysis import Analysis
from app.core.database import AsyncSessionLocal
import time
import hashlib
import json

class SentimentService:
    preprocessor = TextPreprocessor()
    
    @classmethod
    async def analyze(cls, text: str, language: str = "auto", 
                      include_emotions: bool = True,
                      include_toxicity: bool = False,
                      include_entities: bool = False) -> dict:
        """Complete sentiment analysis pipeline"""
        start_time = time.time()
        
        # Preprocess text
        processed = await cls.preprocessor.preprocess_pipeline(text)
        
        # Detect language if auto
        if language == "auto":
            language = processed["language"]
        
        # Get sentiment prediction
        sentiment = await ModelManager.predict_sentiment(processed["cleaned_text"], language)
        
        result = {
            "sentiment": sentiment["sentiment"],
            "confidence": sentiment["confidence"],
            "probabilities": sentiment["probabilities"],
            "language": language,
            "processing_time_ms": (time.time() - start_time) * 1000
        }
        
        # Include emotions if requested
        if include_emotions:
            emotions = await ModelManager.predict_emotions(processed["cleaned_text"])
            result["emotions"] = emotions["all_emotions"]
            result["dominant_emotion"] = emotions["dominant_emotion"]
        
        # Include toxicity if requested
        if include_toxicity:
            toxicity = await ModelManager.detect_toxicity(processed["cleaned_text"])
            result["toxicity"] = toxicity
        
        # Include entities if requested
        if include_entities:
            result["entities"] = processed["entities"]
            result["keywords"] = processed["tokens"][:10]
        
        # Save to database asynchronously
        await cls._save_analysis(text, result, processed)
        
        return result
    
    @classmethod
    async def _save_analysis(cls, original_text: str, result: dict, processed: dict):
        """Save analysis to database"""
        try:
            async with AsyncSessionLocal() as db:
                analysis = Analysis(
                    original_text=original_text[:1000],
                    cleaned_text=processed["cleaned_text"][:1000],
                    language=result.get("language", "unknown"),
                    sentiment_label=result["sentiment"],
                    sentiment_confidence=result["confidence"],
                    sentiment_scores=result["probabilities"],
                    emotions=result.get("emotions"),
                    dominant_emotion=result.get("dominant_emotion"),
                    processing_time_ms=result["processing_time_ms"],
                    entities=result.get("entities")
                )
                db.add(analysis)
                await db.commit()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to save analysis: {e}")
    
    @classmethod
    async def update_user_metrics(cls, user_id: int, result: dict):
        """Update user metrics after analysis"""
        # This would update user's total analyses count, etc.
        pass
    
    @classmethod
    async def batch_analyze(cls, texts: list, **kwargs) -> list:
        """Analyze multiple texts in batch"""
        results = []
        for text in texts:
            result = await cls.analyze(text, **kwargs)
            results.append(result)
        return results