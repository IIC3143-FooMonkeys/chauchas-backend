import pytest
from httpx import AsyncClient
from main import app

URL = "https://www.bozitoapi.online/"
@pytest.mark.asyncio
async def test_fetch_server():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/")
    assert response.json()["message"] == "Hello World"