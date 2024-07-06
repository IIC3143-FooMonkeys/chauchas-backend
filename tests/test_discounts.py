import pytest
from httpx import AsyncClient
from main import app
from bson import ObjectId

URL = "https://www.bozitoapi.online/"
@pytest.mark.asyncio
async def test_get_discounts():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/discounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_try_filters_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        category = response_one.json()[0]["category"]
        response = await ac.get(f"/discounts?category={category}")
    assert response.status_code == 200
    assert response.json()[0]["category"] == category

@pytest.mark.asyncio
async def test_try_filters_cardtype():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        cardType = response_one.json()[0]["cardType"]
        response = await ac.get(f"/discounts?cardType={cardType}")
    assert response.status_code == 200
    assert response.json()[0]["cardType"] == cardType

@pytest.mark.asyncio
async def test_try_filters_bankname():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        bankName = response_one.json()[0]["bankName"]
        response = await ac.get(f"/discounts?bankName={bankName}")
    assert response.status_code == 200
    assert response.json()[0]["bankName"] == bankName

@pytest.mark.asyncio
async def test_get_one_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        discId = response_one.json()[0]["id"]
        response = await ac.get(f"/discounts/{discId}")

    assert response.status_code == 200
    assert response.json()["id"] == discId

@pytest.mark.asyncio
async def test_get_one_invalid_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.get(f"/discounts/{fakeId}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        updateInfo = {
        "id": disc["id"],
        "url": disc["url"],
        "local": disc["local"],
        "discount": disc["discount"] + 5,
        "description": disc["description"],
        "category": disc["category"],
        "expiration": disc["expiration"],
        "days": disc["days"],
        "card": disc["card"],
        "cardType": disc["cardType"],
        "paymentType": disc["paymentType"],
        "bankName": disc["bankName"]
        }
        discId = disc["id"]
        response = await ac.put(f"/discounts/{discId}", json=updateInfo)
    assert response.status_code == 200
    assert response.json()["discount"] == disc["discount"] + 5

@pytest.mark.asyncio
async def test_update_invalid_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        updateInfo = {
            "id": disc["id"],
            "url": disc["url"],
            "local": disc["local"],
            "discount": disc["discount"] + 5,
            "description": disc["description"],
            "category": disc["category"],
            "expiration": disc["expiration"],
            "days": disc["days"],
            "card": disc["card"],
            "cardType": disc["cardType"],
            "paymentType": disc["paymentType"],
            "bankName": disc["bankName"]
        }
        response = await ac.put(f"/discounts/{fakeId}", json=updateInfo)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        discId = disc["id"]
        response = await ac.delete(f"/discounts/{discId}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_invalid_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.delete(f"/discounts/{fakeId}")
    assert response.status_code == 404