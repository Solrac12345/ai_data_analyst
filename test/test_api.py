# EN: Async tests for FastAPI endpoints
# FR: Tests async pour les endpoints FastAPI

import pytest
from httpx import ASGITransport, AsyncClient
from src.api.main import app


@pytest.mark.asyncio
async def test_health_endpoint() -> None:
    """Verify /health returns 200 and correct structure."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.asyncio
async def test_analyze_endpoint_scaffold() -> None:
    """Verify /analyze accepts valid payload and returns pending status."""
    payload = {"data_path": "test.csv"}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
