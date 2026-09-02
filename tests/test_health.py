"""
FOODARA AI - Health Tests
Tests para endpoints de salud.
"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test del endpoint de health check."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "FOODARA AI"


@pytest.mark.asyncio
async def test_info_endpoint():
    """Test del endpoint de información."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "FOODARA AI"
        assert data["country"] == "AR"
        assert data["language"] == "es"


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test del endpoint raíz."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "FOODARA AI" in data["message"]
