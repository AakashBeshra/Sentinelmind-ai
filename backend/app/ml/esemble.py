import numpy as np
from typing import List, Dict, Any
from collections import defaultdict

class ModelEnsemble:
    def __init__(self, models: List[Any], weights: List[float] = None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)
    
    def predict_sentiment(self, text: str) -> Dict[str, Any]:
        """Ensemble prediction for sentiment"""
        predictions = []
        
        for model in self.models:
            pred = model.predict_sentiment(text)
            predictions.append(pred)
        
        return self._ensemble_sentiment(predictions)
    
    def _ensemble_sentiment(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Combine sentiment predictions"""
        sentiment_sums = defaultdict(float)
        
        for weight, pred in zip(self.weights, predictions):
            for sentiment, score in pred.get('probabilities', {}).items():
                sentiment_sums[sentiment] += score * weight
        
        # Normalize
        total = sum(sentiment_sums.values())
        probabilities = {k: v/total for k, v in sentiment_sums.items()}
        
        # Get dominant sentiment
        dominant = max(probabilities.items(), key=lambda x: x[1])
        
        return {
            'sentiment': dominant[0],
            'confidence': dominant[1],
            'probabilities': probabilities,
            'ensemble_method': 'weighted_average'
        }
    
    def predict_emotion(self, text: str) -> Dict[str, Any]:
        """Ensemble prediction for emotions"""
        all_emotions = []
        
        for model in self.models:
            pred = model.predict_emotions(text)
            all_emotions.append(pred.get('all_emotions', {}))
        
        return self._ensemble_emotion(all_emotions)
    
    def _ensemble_emotion(self, all_emotions: List[Dict]) -> Dict[str, Any]:
        """Combine emotion predictions"""
        emotion_sums = defaultdict(float)
        
        for weight, emotions in zip(self.weights, all_emotions):
            for emotion, score in emotions.items():
                emotion_sums[emotion] += score * weight
        
        total = sum(emotion_sums.values())
        if total > 0:
            emotion_sums = {k: v/total for k, v in emotion_sums.items()}
        
        dominant = max(emotion_sums.items(), key=lambda x: x[1]) if emotion_sums else ('unknown', 0)
        
        return {
            'dominant_emotion': dominant[0],
            'dominant_confidence': dominant[1],
            'all_emotions': emotion_sums,
            'ensemble_method': 'weighted_average'
        }