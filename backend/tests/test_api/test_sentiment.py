import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_sentiment_analysis(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/v1/sentiment/analyze", 
        json={"text": "I love this product!"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "confidence" in data

async def test_sentiment_analysis_negative(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/v1/sentiment/analyze",
        json={"text": "This is terrible, I hate it!"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"

async def test_batch_sentiment(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/v1/sentiment/batch",
        json={"texts": ["Good", "Bad", "Okay"]},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3