import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime


class InferenceClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.client = None
    
    async def __aenter__(self):
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=30.0
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def predict_sentiment(self, text: str, include_emotions: bool = True) -> Dict:
        """Send single text for sentiment analysis"""
        response = await self.client.post(
            "/api/v1/sentiment/analyze",
            json={
                "text": text,
                "include_emotions": include_emotions
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def predict_batch(self, texts: List[str], include_emotions: bool = True) -> List[Dict]:
        """Send batch of texts for sentiment analysis"""
        response = await self.client.post(
            "/api/v1/sentiment/batch",
            json={
                "texts": texts,
                "include_emotions": include_emotions
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def detect_emotions(self, text: str) -> Dict:
        """Detect emotions in text"""
        response = await self.client.post(
            "/api/v1/emotion/detect",
            json={"text": text}
        )
        response.raise_for_status()
        return response.json()
    
    async def health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except:
            return False
    
    def predict_sentiment_sync(self, text: str, include_emotions: bool = True) -> Dict:
        """Synchronous version of predict_sentiment"""
        return asyncio.run(self.predict_sentiment(text, include_emotions))
    
    def predict_batch_sync(self, texts: List[str], include_emotions: bool = True) -> List[Dict]:
        """Synchronous version of predict_batch"""
        return asyncio.run(self.predict_batch(texts, include_emotions))


class StreamingClient:
    """Client for WebSocket streaming analysis"""
    
    def __init__(self, base_url: str = "ws://localhost:8000", token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
        self.websocket = None
    
    async def connect(self):
        """Establish WebSocket connection"""
        import websockets
        url = f"{self.base_url}/ws/stream"
        if self.token:
            url += f"?token={self.token}"
        
        self.websocket = await websockets.connect(url)
        return self
    
    async def send_and_receive(self, text: str) -> Dict:
        """Send text and receive analysis"""
        import json
        await self.websocket.send(json.dumps({"text": text}))
        response = await self.websocket.recv()
        return json.loads(response)
    
    async def stream_analysis(self, texts: List[str]):
        """Stream multiple texts for analysis"""
        import json
        results = []
        
        for text in texts:
            await self.websocket.send(json.dumps({"text": text}))
            response = await self.websocket.recv()
            results.append(json.loads(response))
        
        return results
    
    async def close(self):
        """Close WebSocket connection"""
        if self.websocket:
            await self.websocket.close()