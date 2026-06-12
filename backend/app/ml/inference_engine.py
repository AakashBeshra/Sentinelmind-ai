import torch
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
import numpy as np

@dataclass
class InferenceRequest:
    text: str
    task: str
    request_id: str
    timestamp: float

@dataclass
class InferenceResponse:
    request_id: str
    result: Dict[str, Any]
    latency_ms: float
    model_version: str

class InferenceEngine:
    def __init__(self, model_manager, batch_size: int = 32, max_queue_size: int = 1000):
        self.model_manager = model_manager
        self.batch_size = batch_size
        self.request_queue = asyncio.Queue(maxsize=max_queue_size)
        self.results = {}
        self.is_running = True
        self.worker_task = None
    
    async def start(self):
        """Start inference engine worker"""
        self.worker_task = asyncio.create_task(self._process_batches())
    
    async def stop(self):
        """Stop inference engine"""
        self.is_running = False
        if self.worker_task:
            self.worker_task.cancel()
    
    async def predict(self, request: InferenceRequest) -> Dict[str, Any]:
        """Predict single request"""
        future = asyncio.Future()
        self.results[request.request_id] = future
        await self.request_queue.put((request, future))
        return await future
    
    async def _process_batches(self):
        """Process requests in batches"""
        while self.is_running:
            batch = []
            batch_futures = []
            
            try:
                # Collect batch
                for _ in range(self.batch_size):
                    try:
                        request, future = await asyncio.wait_for(
                            self.request_queue.get(), timeout=0.1
                        )
                        batch.append(request)
                        batch_futures.append(future)
                    except asyncio.TimeoutError:
                        break
                
                if batch:
                    await self._process_batch(batch, batch_futures)
            
            except Exception as e:
                print(f"Batch processing error: {e}")
    
    async def _process_batch(self, batch: List[InferenceRequest], futures: List[asyncio.Future]):
        """Process a batch of requests"""
        start_time = time.time()
        
        # Group by task type
        task_groups = {}
        for i, request in enumerate(batch):
            if request.task not in task_groups:
                task_groups[request.task] = []
            task_groups[request.task].append((i, request))
        
        # Process each task group
        results = [None] * len(batch)
        
        for task, items in task_groups.items():
            texts = [item[1].text for item in items]
            
            if task == "sentiment":
                predictions = await self.model_manager.batch_predict(texts, "sentiment")
            elif task == "emotion":
                predictions = await self.model_manager.batch_predict(texts, "emotion")
            elif task == "toxicity":
                predictions = await self.model_manager.batch_predict(texts, "toxicity")
            else:
                predictions = [{"error": f"Unknown task: {task}"} for _ in texts]
            
            for (idx, _), pred in zip(items, predictions):
                results[idx] = pred
        
        # Set results to futures
        latency = (time.time() - start_time) * 1000
        for future, result in zip(futures, results):
            future.set_result(result)