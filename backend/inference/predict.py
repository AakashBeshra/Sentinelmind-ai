import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

class SentimentPredictor:
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
    
    def predict(self, text: str) -> dict:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities, dim=-1)
        
        labels = ["negative", "neutral", "positive"]
        return {
            "sentiment": labels[prediction.item()],
            "confidence": probabilities[0][prediction].item(),
            "probabilities": {
                "negative": probabilities[0][0].item(),
                "neutral": probabilities[0][1].item(),
                "positive": probabilities[0][2].item()
            }
        }

def predict_sentiment(text: str, model_path: str = "../models/sentiment") -> dict:
    predictor = SentimentPredictor(model_path)
    return predictor.predict(text)