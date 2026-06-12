import asyncio
import torch
import logging
from typing import Dict, List, Optional, Any
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
    XLMRobertaForSequenceClassification,
    XLMRobertaTokenizer,
    DistilBertForSequenceClassification,
    DistilBertTokenizer
)
from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache
import hashlib
import json

from app.core.config import settings
from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)

class ModelManager:
    """Centralized model management with caching and optimization"""
    
    _instance = None
    _models = {}
    _tokenizers = {}
    _pipelines = {}
    _device = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    async def load_models(cls):
        """Load all ML models asynchronously"""
        cls._device = torch.device("cuda" if torch.cuda.is_available() and settings.USE_GPU else "cpu")
        logger.info(f"Loading models on: {cls._device}")
        
        # Load sentiment model (XLM-RoBERTa for multilingual support)
        logger.info("Loading sentiment analysis model...")
        cls._models["sentiment"] = XLMRobertaForSequenceClassification.from_pretrained(
            "cardiffnlp/twitter-xlm-roberta-base-sentiment",
            num_labels=3  # positive, negative, neutral
        ).to(cls._device)
        cls._tokenizers["sentiment"] = XLMRobertaTokenizer.from_pretrained(
            "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        )
        cls._models["sentiment"].eval()
        
        # Load emotion detection model
        logger.info("Loading emotion detection model...")
        cls._models["emotion"] = AutoModelForSequenceClassification.from_pretrained(
            "bhadresh-savani/distilbert-base-uncased-emotion",
            num_labels=6  # joy, sadness, anger, fear, love, surprise
        ).to(cls._device)
        cls._tokenizers["emotion"] = DistilBertTokenizer.from_pretrained(
            "bhadresh-savani/distilbert-base-uncased-emotion"
        )
        cls._models["emotion"].eval()
        
        # Load embedding model for semantic analysis
        logger.info("Loading embedding model...")
        cls._models["embedding"] = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2",
            device=cls._device
        )
        
        # Load toxicity detection
        logger.info("Loading toxicity detection model...")
        cls._pipelines["toxicity"] = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            device=0 if torch.cuda.is_available() else -1
        )
        
        logger.info("All models loaded successfully!")
    
    @classmethod
    async def predict_sentiment(cls, text: str, language: str = "auto") -> Dict[str, Any]:
        """Predict sentiment with caching"""
        # Check cache first
        cache_key = f"sentiment:{hashlib.md5(text.encode()).hexdigest()}"
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Tokenize and predict
        inputs = cls._tokenizers["sentiment"](
            text,
            return_tensors="pt",
            truncation=True,
            max_length=settings.MAX_SEQUENCE_LENGTH,
            padding=True
        ).to(cls._device)
        
        with torch.no_grad():
            outputs = cls._models["sentiment"](**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities, dim=-1)
            
            # Map labels (0: negative, 1: neutral, 2: positive)
            labels = ["negative", "neutral", "positive"]
            sentiment = labels[prediction.item()]
            confidence = probabilities[0][prediction].item()
        
        result = {
            "sentiment": sentiment,
            "confidence": confidence,
            "probabilities": {
                "negative": float(probabilities[0][0]),
                "neutral": float(probabilities[0][1]),
                "positive": float(probabilities[0][2])
            }
        }
        
        # Cache result
        await redis_client.setex(cache_key, 3600, json.dumps(result))
        
        return result
    
    @classmethod
    async def predict_emotions(cls, text: str) -> Dict[str, Any]:
        """Detect multiple emotions in text"""
        cache_key = f"emotion:{hashlib.md5(text.encode()).hexdigest()}"
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        inputs = cls._tokenizers["emotion"](
            text,
            return_tensors="pt",
            truncation=True,
            max_length=settings.MAX_SEQUENCE_LENGTH,
            padding=True
        ).to(cls._device)
        
        with torch.no_grad():
            outputs = cls._models["emotion"](**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            emotions = ["sadness", "joy", "love", "anger", "fear", "surprise"]
            emotion_scores = {emotion: float(probabilities[0][i]) for i, emotion in enumerate(emotions)}
            
            # Get dominant emotion
            dominant_emotion = emotions[torch.argmax(probabilities, dim=-1).item()]
            dominant_score = float(torch.max(probabilities, dim=-1)[0][0])
        
        result = {
            "dominant_emotion": dominant_emotion,
            "dominant_confidence": dominant_score,
            "all_emotions": emotion_scores
        }
        
        await redis_client.setex(cache_key, 3600, json.dumps(result))
        
        return result
    
    @classmethod
    async def generate_embedding(cls, text: str) -> List[float]:
        """Generate text embedding for semantic search"""
        embedding = cls._models["embedding"].encode(text, convert_to_tensor=True)
        return embedding.cpu().numpy().tolist()
    
    @classmethod
    async def detect_toxicity(cls, text: str) -> Dict[str, Any]:
        """Detect toxic content"""
        result = cls._pipelines["toxicity"](text)
        return {
            "is_toxic": result[0]["label"] == "toxic",
            "confidence": result[0]["score"]
        }
    
    @classmethod
    async def batch_predict(cls, texts: List[str], task: str = "sentiment") -> List[Dict]:
        """Batch prediction for improved throughput"""
        tasks = []
        for text in texts:
            if task == "sentiment":
                tasks.append(cls.predict_sentiment(text))
            elif task == "emotion":
                tasks.append(cls.predict_emotions(text))
            elif task == "toxicity":
                tasks.append(cls.detect_toxicity(text))
        
        results = await asyncio.gather(*tasks)
        return results
    
    @classmethod
    async def is_healthy(cls) -> bool:
        """Check if models are loaded and responding"""
        try:
            test_result = await cls.predict_sentiment("I love this product!")
            return test_result is not None
        except Exception as e:
            logger.error(f"Model health check failed: {e}")
            return False