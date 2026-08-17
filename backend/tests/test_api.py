import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "market-scrapping-api"}

@pytest.mark.asyncio
async def test_scrape_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "keyword": "minyak goreng",
            "time_range": "monthly",
            "platform": "all",
            "limit": 10
        }
        response = await ac.post("/api/scrape", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "minyak goreng"
    assert len(data["data"]) == 10
    assert data["data"][0]["rank"] == 1
