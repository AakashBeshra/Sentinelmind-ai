# SentinelMind AI - Advanced Sentiment Analysis Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)

---

## 🚀 Overview

SentinelMind AI is an advanced, production-ready sentiment analysis platform that combines traditional NLP techniques with intelligent sarcasm detection.

The platform provides:

- Sentiment Analysis
- Emotion Detection
- Sarcasm Recognition
- Real-time Processing
- REST API Integration
- Interactive Dashboard
- Confidence Scoring

---

## ✨ Key Features

- Sentiment Analysis (Positive, Negative, Neutral)
- Sarcasm Detection
- Emotion Analysis
- Confidence Scoring
- Real-time Processing
- Interactive Dashboard
- REST API
- Modern UI
- Dark/Light Mode Support

---

## 🏗️ Architecture

    ┌─────────────────────────────────────────────────────────────┐
    │ Client Applications                                         │
    ├──────────────────────────┬──────────────────────────────────┤
    │ Next.js Web App          │ REST API Clients                │
    │ (Port 3000)             │                                 │
    └────────────┬─────────────┴───────────────┬──────────────────┘
                 │                             │
                 └───────────────┬─────────────┘
                                 │
                         ┌───────▼────────┐
                         │ FastAPI API    │
                         │ (Port 8000)    │
                         └───────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
         ┌────▼────┐      ┌─────▼─────┐      ┌────▼────┐
         │ SQLite  │      │ Redis     │      │ Models  │
         │ Database│      │ Cache     │      │ NLP     │
         └─────────┘      └───────────┘      └─────────┘

---

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- npm
- Git
- Docker (Optional)

---

## 🛠️ Installation

### Backend Setup

    cd backend

    python -m venv venv

    Windows:
    .\venv\Scripts\activate

    Linux / Mac:
    source venv/bin/activate

    pip install -r requirements.txt

---

### Required Python Packages

    pip install fastapi uvicorn
    pip install textblob
    pip install sqlalchemy aiosqlite
    pip install pydantic pydantic-settings
    pip install python-multipart
    pip install python-dotenv

---

### Frontend Setup

    cd frontend

    npm install

    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

---

## 🚀 Running the Application

### Start Backend

    cd backend

    Windows:
    .\venv\Scripts\activate

    Linux / Mac:
    source venv/bin/activate

    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Backend URL:

    http://localhost:8000

---

### Start Frontend

    cd frontend

    npm run dev

Frontend URL:

    http://localhost:3000

---

## 📊 API Documentation

Interactive Documentation:

    Swagger UI:
    http://localhost:8000/docs

    ReDoc:
    http://localhost:8000/redoc

---

## API Endpoints

| Method | Endpoint | Description |
|----------|----------|----------|
| GET | / | Root Endpoint |
| GET | /health | Health Check |
| POST | /api/v1/sentiment/analyze | Analyze Sentiment |

---

## Example API Request

    curl -X POST "http://localhost:8000/api/v1/sentiment/analyze" \
      -H "Content-Type: application/json" \
      -d '{
        "text":"I love this product!",
        "language":"auto",
        "include_emotions":true
      }'

---

## Example API Response

    {
      "sentiment": "positive",
      "confidence": 0.85,
      "probabilities": {
        "positive": 0.85,
        "negative": 0.05,
        "neutral": 0.10
      },
      "emotions": {
        "joy": 0.42,
        "sadness": 0.08,
        "anger": 0.05,
        "fear": 0.05,
        "love": 0.25,
        "surprise": 0.15
      },
      "language": "en",
      "processing_time_ms": 45.2
    }

---

## 🧪 Testing the Application

### Sample Texts

| Text | Expected Sentiment |
|--------|--------|
| I absolutely love this amazing product! | Positive |
| This is terrible, I hate it | Negative |
| The weather is okay I guess | Neutral |
| Great job, you really screwed that up | Negative (Sarcasm) |

---

### Health Check

    curl http://localhost:8000/health

Expected Response:

    {
      "status": "healthy"
    }

---

## 🔧 Configuration

### Backend (.env)

    APP_NAME=SentinelMind AI
    ENVIRONMENT=development
    DEBUG=True
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=sqlite+aiosqlite:///./sentinelmind.db
    CORS_ORIGINS=["http://localhost:3000"]

---

### Frontend (.env.local)

    NEXT_PUBLIC_API_URL=http://localhost:8000

---

## 🐳 Docker Setup (Optional)

### Start Redis

    docker run -d --name sentinelmind-redis -p 6379:6379 redis:alpine

---

## 📁 Project Structure

    sentinelmind-ai/
    ├── backend/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── core/
    │   │   ├── api/
    │   │   └── models/
    │   ├── requirements.txt
    │   └── .env
    │
    ├── frontend/
    │   ├── app/
    │   │   ├── page.tsx
    │   │   └── layout.tsx
    │   ├── components/
    │   ├── package.json
    │   └── .env.local
    │
    └── README.md

---

## 🤝 Contributing

    git checkout -b feature/amazing-feature

    git commit -m "Add amazing feature"

    git push origin feature/amazing-feature

Create a Pull Request after pushing changes.

---

## 📝 Development Notes

### Sarcasm Detection

Features:

- Contradictory statement detection
- Common sarcasm pattern recognition
- Sentiment score adjustment

---

### Emotion Analysis

Detected Emotions:

😊 Joy

😢 Sadness

😠 Anger

😨 Fear

❤️ Love

😲 Surprise

---

## ⚠️ Troubleshooting

### Port Already In Use

    netstat -ano | findstr :8000

    taskkill /PID <PID> /F

---

### Module Not Found

    pip install --upgrade pip

    pip install -r requirements.txt

---

### CORS Errors

Verify:

- Backend CORS configuration
- Frontend API URL
- Backend running status

---

## 🚀 Deployment

### Production Backend

    cd backend

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

---

### Production Frontend

    cd frontend

    npm run build

    npm start

---

## 📄 License

MIT License

See LICENSE file for details.

---

## 🙏 Acknowledgments

- TextBlob
- FastAPI
- Next.js
- Open Source Contributors

---

## 📞 Support

Issues:
GitHub Issues

Documentation:
API Documentation

---

## 🎉 Success

Once both servers are running:

    http://localhost:3000

The platform will:

- Accept text input
- Analyze sentiment
- Detect sarcasm
- Identify emotions
- Display confidence scores

Enjoy using SentinelMind AI! 🚀❤️

---

## README Includes

✅ Installation Instructions

✅ API Documentation

✅ Example Requests & Responses

✅ Testing Guide

✅ Troubleshooting

✅ Project Structure

✅ Deployment Notes

✅ Feature Documentation