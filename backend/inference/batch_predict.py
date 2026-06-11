import asyncio
from typing import List, Dict, Any
from datetime import datetime
import json
import os

from app.ml.model_manager import ModelManager
from app.services.sentiment_service import SentimentService
from app.core.logging import logger


class BatchPredictor:
    def __init__(self, batch_size: int = 32, max_concurrent: int = 5):
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.results = []
    
    async def predict_batch(self, texts: List[str], task: str = "sentiment") -> List[Dict]:
        """Process batch of texts for sentiment/emotion analysis"""
        results = []
        
        # Split into smaller batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_results = await self._process_batch(batch, task)
            results.extend(batch_results)
            
            logger.info(f"Processed batch {i // self.batch_size + 1}/{(len(texts) - 1) // self.batch_size + 1}")
        
        return results
    
    async def _process_batch(self, batch: List[str], task: str) -> List[Dict]:
        """Process a single batch"""
        tasks = []
        
        for text in batch:
            if task == "sentiment":
                tasks.append(ModelManager.predict_sentiment(text))
            elif task == "emotion":
                tasks.append(ModelManager.predict_emotions(text))
            else:
                tasks.append(SentimentService.analyze(text))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({"error": str(result)})
            else:
                processed_results.append(result)
        
        return processed_results
    
    def predict_batch_sync(self, texts: List[str], task: str = "sentiment") -> List[Dict]:
        """Synchronous version of batch prediction"""
        return asyncio.run(self.predict_batch(texts, task))
    
    async def predict_from_file(self, file_path: str, task: str = "sentiment") -> List[Dict]:
        """Read texts from file and process batch"""
        texts = []
        
        # Determine file type from extension
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        
        elif file_path.endswith('.csv'):
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                text_col = headers[0] if headers else 'text'
                for row in reader:
                    if row:
                        texts.append(row[0])
        
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    texts = [item.get('text', str(item)) for item in data]
                elif isinstance(data, dict):
                    texts = list(data.values())
        
        return await self.predict_batch(texts, task)
    
    def save_results(self, results: List[Dict], output_path: str, format: str = "json"):
        """Save batch results to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.utcnow().isoformat(),
                    "total": len(results),
                    "results": results
                }, f, indent=2)
        
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if results:
                    fieldnames = list(results[0].keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
        
        logger.info(f"Results saved to {output_path}")


# Singleton instance
batch_predictor = BatchPredictor()


async def batch_predict(texts: List[str], task: str = "sentiment") -> List[Dict]:
    """Convenience function for batch prediction"""
    return await batch_predictor.predict_batch(texts, task)