from textblob import TextBlob
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict
import time
import re
import hashlib
import json
from collections import OrderedDict

app = FastAPI(title="SentinelMind AI")

# Simple in-memory cache (for demo purposes)
# In production, use Redis
class SimpleCache:
    def __init__(self, max_size=100):
        self.cache = OrderedDict()
        self.max_size = max_size
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
    
    def clear(self):
        self.cache.clear()

cache = SimpleCache()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    print(f"[REQUEST] {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Log response
    process_time = (time.time() - start_time) * 1000
    print(f"[RESPONSE] {response.status_code} - {process_time:.2f}ms")
    
    response.headers["X-Process-Time-MS"] = str(int(process_time))
    return response

# Request model for sentiment analysis
class SentimentRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"
    include_emotions: Optional[bool] = True
    include_toxicity: Optional[bool] = False

# Response model for sentiment analysis
class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    probabilities: Dict[str, float]
    emotions: Optional[Dict[str, float]] = None
    language: str
    processing_time_ms: float

@app.get("/")
async def root():
    return {"message": "SentinelMind AI is running!", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/cache/stats")
async def cache_stats():
    """Get cache statistics (for debugging)"""
    return {
        "cache_size": len(cache.cache),
        "max_size": cache.max_size,
        "keys": list(cache.cache.keys())[:10]  # Show first 10 keys
    }

@app.delete("/api/v1/cache")
async def clear_cache():
    """Clear the response cache"""
    cache.clear()
    return {"message": "Cache cleared successfully"}

def detect_sarcasm(text: str) -> tuple:
    """Detect sarcasm in text"""
    text_lower = text.lower()
    
    # Sarcasm patterns
    sarcasm_patterns = [
        r'good.*?but', r'great.*?however', r'ice.*?except',
        r'you smell like', r'you look like', r'sure you do',
        r'right.*?as if', r'yeah.*?sure', r'obviously.*?not'
    ]
    
    # Sarcasm indicators
    sarcasm_words = ['smell', 'poop', 'stupid', 'dumb', 'idiot', 'moron', 
                     'pathetic', 'useless', 'worthless', 'terrible',
                     'horrible', 'disgusting', 'awful', 'waste']
    
    # Positive words that might indicate sarcasm when paired with negative
    positive_words = ['good', 'great', 'nice', 'awesome', 'amazing', 'wonderful', 'excellent', 'brilliant', 'perfect', 'superb', 'fantastic']
    
    has_positive = any(word in text_lower for word in positive_words)
    has_negative = any(word in text_lower for word in sarcasm_words)
    has_sarcasm_pattern = any(re.search(pattern, text_lower) for pattern in sarcasm_patterns)
    
    # Check for contradiction (positive word + negative word)
    if has_positive and has_negative:
        return True, 0.85
    if has_sarcasm_pattern:
        return True, 0.75
    
    return False, 0.0

def get_sentiment_textblob(text: str, is_sarcastic: bool = False) -> tuple:
    """Get sentiment using TextBlob with sarcasm adjustment"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # If sarcastic, flip the sentiment
    if is_sarcastic:
        polarity = -polarity
    
    if polarity > 0:
        positive_score = min(0.95, polarity)
        negative_score = max(0.01, (1 - polarity) * 0.3)
        neutral_score = 1 - (positive_score + negative_score)
        sentiment = "positive"
    elif polarity < 0:
        negative_score = min(0.95, abs(polarity))
        positive_score = max(0.01, (1 - abs(polarity)) * 0.3)
        neutral_score = 1 - (positive_score + negative_score)
        sentiment = "negative"
    else:
        positive_score = 0.15
        negative_score = 0.15
        neutral_score = 0.70
        sentiment = "neutral"
    
    total = positive_score + negative_score + neutral_score
    positive_score = round(positive_score / total, 3)
    negative_score = round(negative_score / total, 3)
    neutral_score = round(neutral_score / total, 3)
    
    confidence = max(positive_score, negative_score, neutral_score)
    
    return sentiment, confidence, {
        "positive": positive_score,
        "negative": negative_score,
        "neutral": neutral_score
    }

def detect_emotions(text: str, is_sarcastic: bool = False) -> Dict[str, float]:
    """Enhanced emotion detection with sarcasm adjustment"""
    text_lower = text.lower()
    
    emotion_keywords = {
        "joy": ["happy", "joy", "delighted", "pleased", "glad", "cheerful", "joyful", "wonderful", "amazing", "excellent", "creative", "appreciate", "great", "good", "beautiful", "fantastic", "awesome", "brilliant"],
        "sadness": ["sad", "depressed", "unhappy", "miserable", "gloomy", "disappointed", "heartbroken", "lonely", "hurt", "crying"],
        "anger": ["angry", "mad", "furious", "annoyed", "irritated", "hate", "rage", "frustrated", "upset", "frustrating"],
        "fear": ["afraid", "scared", "terrified", "worried", "anxious", "nervous", "fear", "panic", "concerned", "stress"],
        "love": ["love", "adore", "cherish", "affection", "care", "fond", "passion", "romantic", "appreciate", "admire", "respect", "like"],
        "surprise": ["surprised", "shocked", "astonished", "amazed", "unexpected", "wow", "oh", "crazy", "incredible", "unbelievable", "stunning"]
    }
    
    scores = {emotion: 0.1 for emotion in emotion_keywords}
    
    for emotion, keywords in emotion_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        if matches > 0:
            scores[emotion] = min(0.9, 0.2 + (matches * 0.12))
    
    # If sarcastic, reduce joy/positive emotions and increase negative ones
    if is_sarcastic:
        scores["joy"] = max(0.05, scores["joy"] - 0.4)
        scores["love"] = max(0.05, scores["love"] - 0.3)
        scores["anger"] = min(0.8, scores["anger"] + 0.3)
        scores["sadness"] = min(0.8, scores["sadness"] + 0.2)
    
    total = sum(scores.values())
    if total > 0:
        scores = {k: round(v / total, 3) for k, v in scores.items()}
    
    return scores

@app.post("/api/v1/sentiment/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text using TextBlob with sarcasm detection
    """
    start_time = time.time()
    
    text = request.text
    
    # Generate cache key based on text and options
    cache_key = hashlib.md5(
        f"{text}_{request.include_emotions}".encode()
    ).hexdigest()
    
    # Check cache
    cached_result = cache.get(cache_key)
    if cached_result:
        print(f"[CACHE HIT] Returning cached result for: {text[:50]}...")
        return cached_result
    
    # First check for sarcasm
    is_sarcastic, sarcasm_confidence = detect_sarcasm(text)
    
    # Get sentiment with sarcasm adjustment
    sentiment, confidence, probabilities = get_sentiment_textblob(text, is_sarcastic)
    
    # Add sarcasm note to response header or log
    if is_sarcastic:
        probabilities["sarcasm_detected"] = sarcasm_confidence
    
    # Detect emotions with sarcasm adjustment
    emotions = None
    if request.include_emotions:
        emotions = detect_emotions(text, is_sarcastic)
    
    processing_time = (time.time() - start_time) * 1000
    
    response = SentimentResponse(
        sentiment=sentiment,
        confidence=confidence,
        probabilities=probabilities,
        emotions=emotions,
        language=request.language if request.language != "auto" else "en",
        processing_time_ms=round(processing_time, 2)
    )
    
    # Store in cache
    cache.set(cache_key, response)
    
    return response

@app.post("/api/v1/sentiment/upload")
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    include_emotions: bool = True
):
    """
    Upload a text file for sentiment analysis
    Supports: .txt, .csv (first column), .json (text field)
    """
    start_time = time.time()
    
    # Validate file type
    allowed_extensions = ['.txt', '.csv', '.json']
    file_extension = f".{file.filename.split('.')[-1].lower()}"
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Read file content
    content = await file.read()
    
    try:
        text_content = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    
    # Parse based on file type
    if file_extension == '.txt':
        texts = [line.strip() for line in text_content.split('\n') if line.strip()]
        
    elif file_extension == '.csv':
        import csv
        import io
        csv_reader = csv.reader(io.StringIO(text_content))
        texts = []
        for row in csv_reader:
            if row:
                texts.append(row[0])  # Use first column
        
    elif file_extension == '.json':
        try:
            data = json.loads(text_content)
            if isinstance(data, list):
                texts = [str(item) for item in data]
            elif isinstance(data, dict):
                texts = [str(data.get('text', str(data)))]
            else:
                texts = [str(data)]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    else:
        texts = [text_content]
    
    # Limit number of texts to prevent abuse
    if len(texts) > 50:
        texts = texts[:50]
    
    # Analyze each text
    results = []
    for i, text in enumerate(texts):
        if text.strip():
            sentiment, confidence, probabilities = get_sentiment_textblob(text)
            
            emotions = None
            if include_emotions:
                emotions = detect_emotions(text)
            
            results.append({
                "index": i,
                "text": text[:200] + ("..." if len(text) > 200 else ""),
                "sentiment": sentiment,
                "confidence": confidence,
                "probabilities": probabilities,
                "emotions": emotions
            })
    
    processing_time = (time.time() - start_time) * 1000
    
    return {
        "filename": file.filename,
        "total_lines": len(texts),
        "analyzed": len(results),
        "results": results,
        "processing_time_ms": round(processing_time, 2)
    }

@app.get("/api/v1/sentiment/health")
async def sentiment_health():
    """Check if sentiment analysis is working"""
    test_result = get_sentiment_textblob("This is great!")
    return {
        "status": "healthy",
        "test_result": test_result[0],
        "sarcasm_detection": True,
        "emotion_detection": True
    }
