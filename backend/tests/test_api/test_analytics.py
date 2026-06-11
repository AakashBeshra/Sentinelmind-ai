import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


pytestmark = pytest.mark.asyncio


async def test_get_dashboard_stats(client, auth_token):
    """Test dashboard statistics endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await client.get("/api/v1/analytics/dashboard", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "total_analyses" in data
    assert "sentiment_distribution" in data


async def test_get_sentiment_trends(client, auth_token):
    """Test sentiment trends endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await client.get(
        "/api/v1/analytics/trends?days=30",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "trends" in data
    assert "overall_trend" in data


async def test_get_emotion_distribution(client, auth_token):
    """Test emotion distribution endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await client.get(
        "/api/v1/analytics/emotion-distribution?days=30",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "distribution" in data or "counts" in data


async def test_get_top_keywords(client, auth_token):
    """Test top keywords endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await client.get(
        "/api/v1/analytics/top-keywords?limit=10",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "keywords" in data


async def test_export_analytics(client, auth_token):
    """Test analytics export endpoint"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    export_data = {
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-31T23:59:59",
        "format": "json"
    }
    
    response = await client.post(
        "/api/v1/analytics/export",
        json=export_data,
        headers=headers
    )
    
    assert response.status_code == 200
    assert "export_url" in response.json()