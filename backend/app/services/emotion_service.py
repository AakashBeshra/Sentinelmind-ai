from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

from app.ml.model_manager import ModelManager
from app.nlp.preprocessor import TextPreprocessor
from app.core.redis_client import redis_client
import hashlib
import json

class EmotionService:
    preprocessor = TextPreprocessor()
    
    # Emotion intensity mapping
    INTENSITY_THRESHOLDS = {
        "low": 0.33,
        "medium": 0.66,
        "high": 1.0
    }
    
    # Emotions with their associated colors and tips
    EMOTION_INFO = {
        "joy": {
            "color": "#FFD700",
            "tip": "Great! Keep spreading positivity!",
            "suggestions": ["Share your happiness", "Express gratitude", "Celebrate achievements"]
        },
        "sadness": {
            "color": "#4A90E2",
            "tip": "It's okay to feel sad. Take time for self-care.",
            "suggestions": ["Talk to someone", "Practice mindfulness", "Take a break"]
        },
        "anger": {
            "color": "#E74C3C",
            "tip": "Take a deep breath. Consider reframing your message.",
            "suggestions": ["Step away for a moment", "Practice deep breathing", "Write your feelings down"]
        },
        "fear": {
            "color": "#8E44AD",
            "tip": "It's natural to feel concerned. Focus on what you can control.",
            "suggestions": ["Identify specific concerns", "Make a plan", "Seek support"]
        },
        "love": {
            "color": "#FF69B4",
            "tip": "Beautiful! Spread the love!",
            "suggestions": ["Express appreciation", "Connect with loved ones", "Share kindness"]
        },
        "surprise": {
            "color": "#F39C12",
            "tip": "Unexpected moments can lead to new opportunities!",
            "suggestions": ["Embrace the unexpected", "Stay curious", "Explore new possibilities"]
        }
    }
    
    @classmethod
    async def detect_emotions(cls, text: str, language: str = "auto") -> Dict:
        """Detect emotions in text with detailed analysis"""
        # Preprocess text
        processed = await cls.preprocessor.preprocess_pipeline(text)
        
        # Get emotion prediction
        emotion_result = await ModelManager.predict_emotions(processed["cleaned_text"])
        
        # Calculate emotional intensity
        intensity = cls.calculate_intensity(emotion_result["dominant_confidence"])
        
        # Get contextual recommendations
        recommendations = cls.get_recommendation(
            emotion_result["dominant_emotion"],
            intensity
        )
        
        # Calculate emotional volatility (how mixed the emotions are)
        volatility = cls.calculate_volatility(emotion_result["all_emotions"])
        
        return {
            "dominant_emotion": emotion_result["dominant_emotion"],
            "dominant_confidence": emotion_result["dominant_confidence"],
            "all_emotions": emotion_result["all_emotions"],
            "intensity": intensity,
            "volatility": volatility,
            "recommendations": recommendations,
            "emotion_info": cls.EMOTION_INFO.get(emotion_result["dominant_emotion"], {}),
            "processing_time_ms": processed.get("processing_time", 0)
        }
    
    @classmethod
    def calculate_intensity(cls, confidence: float) -> str:
        """Calculate emotional intensity level"""
        for level, threshold in cls.INTENSITY_THRESHOLDS.items():
            if confidence <= threshold:
                return level
        return "high"
    
    @classmethod
    def calculate_volatility(cls, emotions: Dict[str, float]) -> float:
        """Calculate emotional volatility (standard deviation of emotion scores)"""
        scores = list(emotions.values())
        if not scores:
            return 0.0
        return float(np.std(scores))
    
    @classmethod
    def get_recommendation(cls, emotion: str, intensity: str) -> List[str]:
        """Get personalized recommendations based on emotion and intensity"""
        base_recommendations = cls.EMOTION_INFO.get(emotion, {}).get("suggestions", [])
        
        if intensity == "high":
            return [f"⚡ {rec}" for rec in base_recommendations]
        elif intensity == "low":
            return [f"💭 {rec}" for rec in base_recommendations[:2]]
        return base_recommendations
    
    @classmethod
    async def track_emotion_timeline(cls, user_id: int, text: str) -> Dict:
        """Track emotion changes over time for a user"""
        # Get current emotion
        current = await cls.detect_emotions(text)
        
        # Get previous emotion from Redis
        cache_key = f"emotion_timeline:{user_id}"
        previous_data = await redis_client.get(cache_key)
        
        timeline = []
        if previous_data:
            previous = json.loads(previous_data)
            timeline = previous.get("timeline", [])
        
        # Add current to timeline
        timeline.append({
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": current["dominant_emotion"],
            "confidence": current["dominant_confidence"],
            "intensity": current["intensity"]
        })
        
        # Keep last 100 entries
        timeline = timeline[-100:]
        
        # Calculate trend
        trend = cls._calculate_emotion_trend(timeline)
        
        # Store back to Redis
        await redis_client.setex(
            cache_key,
            86400,  # 24 hours
            json.dumps({"timeline": timeline, "trend": trend})
        )
        
        return {
            "current_emotion": current,
            "timeline": timeline[-10:],  # Last 10 entries
            "trend": trend
        }
    
    @classmethod
    def _calculate_emotion_trend(cls, timeline: List[Dict]) -> str:
        """Calculate emotion trend direction"""
        if len(timeline) < 2:
            return "stable"
        
        # Map emotions to numeric values (simplified)
        emotion_values = {
            "joy": 5, "love": 4, "surprise": 3, 
            "fear": 2, "sadness": 1, "anger": 0
        }
        
        recent = timeline[-5:] if len(timeline) >= 5 else timeline
        values = [emotion_values.get(entry["emotion"], 3) for entry in recent]
        
        if len(values) < 2:
            return "stable"
        
        # Calculate slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.2:
            return "improving"
        elif slope < -0.2:
            return "declining"
        else:
            return "stable"
    
    @classmethod
    async def multimodal_analysis(cls, text: str = None, voice_features: Dict = None, 
                                  facial_features: Dict = None) -> Dict:
        """Combine text, voice, and facial expressions for emotion detection"""
        modality_scores = []
        weights = {"text": 0.5, "voice": 0.3, "facial": 0.2}
        
        # Text emotion
        if text:
            text_emotions = await cls.detect_emotions(text)
            modality_scores.append(("text", text_emotions["all_emotions"]))
        
        # Voice emotion (simplified - would use audio features in production)
        if voice_features:
            voice_emotions = cls._analyze_voice_emotion(voice_features)
            modality_scores.append(("voice", voice_emotions))
        
        # Facial expression emotion
        if facial_features:
            facial_emotions = cls._analyze_facial_emotion(facial_features)
            modality_scores.append(("facial", facial_emotions))
        
        # Fuse modalities
        fused_emotions = {}
        for emotion in cls.EMOTION_INFO.keys():
            weighted_score = 0
            total_weight = 0
            
            for modality, scores in modality_scores:
                weight = weights.get(modality, 0.33)
                weighted_score += scores.get(emotion, 0) * weight
                total_weight += weight
            
            if total_weight > 0:
                fused_emotions[emotion] = weighted_score / total_weight
        
        # Get dominant emotion
        dominant = max(fused_emotions.items(), key=lambda x: x[1])
        
        return {
            "dominant_emotion": dominant[0],
            "dominant_confidence": dominant[1],
            "all_emotions": fused_emotions,
            "modalities_used": [m[0] for m in modality_scores],
            "fusion_method": "weighted_average"
        }
    
    @classmethod
    def _analyze_voice_emotion(cls, features: Dict) -> Dict[str, float]:
        """Analyze emotion from voice features (pitch, tone, etc.)"""
        # Simplified - would use actual ML model in production
        pitch = features.get("pitch", 0)
        energy = features.get("energy", 0)
        
        emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "love": 0.0,
            "surprise": 0.0
        }
        
        # Simple rule-based mapping
        if pitch > 200:
            emotions["joy"] = min(1.0, pitch / 500)
        elif pitch < 100:
            emotions["sadness"] = min(1.0, (100 - pitch) / 100)
        
        if energy > 0.7:
            emotions["anger"] = energy
            emotions["surprise"] = energy * 0.5
        
        return emotions
    
    @classmethod
    def _analyze_facial_emotion(cls, features: Dict) -> Dict[str, float]:
        """Analyze emotion from facial expressions"""
        # Simplified - would use computer vision model in production
        facial_emotions = {
            "joy": features.get("smile", 0),
            "sadness": features.get("frown", 0),
            "anger": features.get("brow_furrow", 0),
            "fear": features.get("wide_eyes", 0),
            "surprise": features.get("raised_eyebrows", 0)
        }
        
        # Normalize
        total = sum(facial_emotions.values())
        if total > 0:
            facial_emotions = {k: v/total for k, v in facial_emotions.items()}
        
        return facial_emotions