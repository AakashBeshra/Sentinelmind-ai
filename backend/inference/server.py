import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from app.ml.model_manager import ModelManager
from app.core.config import settings


class PredictRequest(BaseModel):
    text: str
    include_emotions: bool = True


class BatchPredictRequest(BaseModel):
    texts: List[str]
    include_emotions: bool = True


class InferenceServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 9000):
        self.host = host
        self.port = port
        self.app = FastAPI(title="SentinelMind Inference Server", version="1.0.0")
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.on_event("startup")
        async def startup_event():
            await ModelManager.load_models()
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy", "models_loaded": True}
        
        @self.app.post("/predict/sentiment")
        async def predict_sentiment(request: PredictRequest):
            """Single sentiment prediction"""
            result = await ModelManager.predict_sentiment(
                request.text,
                include_emotions=request.include_emotions
            )
            return result
        
        @self.app.post("/predict/batch")
        async def predict_batch(request: BatchPredictRequest):
            """Batch sentiment prediction"""
            results = []
            for text in request.texts:
                result = await ModelManager.predict_sentiment(
                    text,
                    include_emotions=request.include_emotions
                )
                results.append(result)
            return {"results": results, "total": len(results)}
        
        @self.app.post("/predict/emotion")
        async def predict_emotion(request: PredictRequest):
            """Single emotion prediction"""
            result = await ModelManager.predict_emotions(request.text)
            return result
    
    def run(self):
        """Start the inference server"""
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )


def start_inference_server():
    """Convenience function to start server"""
    server = InferenceServer()
    server.run()


if __name__ == "__main__":
    start_inference_server()