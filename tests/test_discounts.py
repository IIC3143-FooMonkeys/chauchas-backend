import pytest
from httpx import AsyncClient
from main import app
from bson import ObjectId
from .admin_info import admin
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
async def test_try_filters_paymentmethod():
    async with AsyncClient(app=app, base_url=URL) as ac:
        look_card_response = await ac.get(f"/cards")
        paymentMethod = look_card_response.json()[0]["paymentMethod"]
        response = await ac.get(f"/discounts?paymentMethod={paymentMethod}")
    assert response.status_code == 200
    assert response.json()[0]["paymentMethod"] == paymentMethod


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
        "imageUrl": disc["imageUrl"],
        "local": disc["local"],
        "discount": disc["discount"] + 5,
        "description": disc["description"],
        "category": disc["category"],
        "expiration": disc["expiration"],
        "days": disc["days"],
        "card": disc["card"],
        "cardType": disc["cardType"],
        "paymentMethod": disc["paymentMethod"],
        "bankName": disc["bankName"]
        }
        discId = disc["id"]
        response = await ac.put(f"/discounts/{discId}?userId={admin}", json=updateInfo)
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
            "imageUrl": disc["imageUrl"],
            "local": disc["local"],
            "discount": disc["discount"] + 5,
            "description": disc["description"],
            "category": disc["category"],
            "expiration": disc["expiration"],
            "days": disc["days"],
            "card": disc["card"],
            "cardType": disc["cardType"],
            "paymentMethod": disc["paymentMethod"],
            "bankName": disc["bankName"]
        }
        response = await ac.put(f"/discounts/{fakeId}?userId={admin}", json=updateInfo)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        discId = disc["id"]
        response = await ac.delete(f"/discounts/{discId}?userId={admin}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_invalid_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.delete(f"/discounts/{fakeId}?userId={admin}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_discount():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        discId = disc["id"]
        response = await ac.delete(f"/discounts/{discId}?userId={admin}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_discount_invalid_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        discId = disc["id"]
        response = await ac.delete(f"/discounts/{discId}?userId={fakeId}")
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_delete_discount_unauthorized():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": [], "userType": 0}
        creation_response_1 = await ac.post(f"/users?userId={admin}", json=user_data)
        validUser = creation_response_1.json()["auth0Id"]
        response_one = await ac.get("/discounts")
        disc = response_one.json()[0]
        discId = disc["id"]
        response = await ac.delete(f"/discounts/{discId}?userId={validUser}")
    assert response.status_code == 403