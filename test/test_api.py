# EN: Async integration tests for FastAPI endpoints
# FR: Tests d'intégration async pour les endpoints FastAPI

import pandas as pd
import pytest
from httpx import ASGITransport, AsyncClient
from pathlib import Path
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
async def test_analyze_endpoint_success(tmp_path: Path) -> None:
    """Verify /analyze runs the pipeline and returns insights."""
    csv_file = tmp_path / "data.csv"
    pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}).to_csv(csv_file, index=False)

    payload = {
        "data_path": str(csv_file),
        "output_dir": str(tmp_path / "output"),
        "report_path": str(tmp_path / "report.html"),
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/analyze", json=payload, timeout=30.0)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["insights"]) > 0
    assert data["report_url"] == payload["report_path"]


@pytest.mark.asyncio
async def test_analyze_endpoint_missing_file() -> None:
    """Verify /analyze handles missing files gracefully."""
    payload = {"data_path": "nonexistent.csv"}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "not found" in data["message"].lower()
