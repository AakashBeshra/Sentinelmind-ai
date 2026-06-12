from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
ACTIVE_REQUESTS = Gauge('active_requests', 'Active HTTP requests')

MODEL_INFERENCE_TIME = Histogram('model_inference_seconds', 'Model inference time', ['model_name'])
MODEL_INFERENCE_COUNT = Counter('model_inference_total', 'Total model inferences', ['model_name', 'status'])

DATABASE_CONNECTION_COUNT = Gauge('database_connections', 'Number of active database connections')
REDIS_CONNECTION_COUNT = Gauge('redis_connections', 'Number of active Redis connections')

class MetricsMiddleware:
    async def __call__(self, request, call_next):
        ACTIVE_REQUESTS.inc()
        start_time = time.time()
        
        response = await call_next(request)
        
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        ACTIVE_REQUESTS.dec()
        
        return response