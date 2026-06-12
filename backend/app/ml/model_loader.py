import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    XLMRobertaForSequenceClassification,
    XLMRobertaTokenizer
)
import os
import json
from typing import Dict, Any

class ModelLoader:
    @staticmethod
    def load_sentiment_model(model_path: str, device: str = "cpu"):
        """Load sentiment analysis model"""
        try:
            model = XLMRobertaForSequenceClassification.from_pretrained(model_path)
            tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
            
            model.to(device)
            model.eval()
            
            return model, tokenizer
        except Exception as e:
            print(f"Error loading sentiment model: {e}")
            return None, None
    
    @staticmethod
    def load_emotion_model(model_path: str, device: str = "cpu"):
        """Load emotion detection model"""
        try:
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            model.to(device)
            model.eval()
            
            return model, tokenizer
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            return None, None
    
    @staticmethod
    def load_onnx_model(model_path: str):
        """Load ONNX model for faster inference"""
        try:
            import onnxruntime as ort
            session = ort.InferenceSession(model_path)
            return session
        except Exception as e:
            print(f"Error loading ONNX model: {e}")
            return None
    
    @staticmethod
    def get_model_metadata(model_path: str) -> Dict[str, Any]:
        """Load model metadata"""
        metadata_path = os.path.join(model_path, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return {}