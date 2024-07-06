import pytest
from httpx import AsyncClient
from main import app
from bson import ObjectId

URL = "https://www.bozitoapi.online/"
@pytest.mark.asyncio
async def test_get_cards():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/cards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_read_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una tarjeta primero para obtener su id
        getabank = await ac.get("/banks")
        bankId = getabank.json()[0]["id"]
        bankName = getabank.json()[0]["name"]
        card_data = {"bankId": bankId, "cardType": "TestType", "bankName": bankName, "paymentMethod": "Credito","id":""}
        create_response = await ac.post("/cards", json=card_data)
        card_id = create_response.json()["id"]

        # Ahora lee la tarjeta
        response = await ac.get(f"/cards/{card_id}")
    assert response.status_code == 200
    assert response.json()["cardType"] == "TestType"

@pytest.mark.asyncio
async def test_read_unexistent_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())

        # Ahora lee la tarjeta
        response = await ac.get(f"/cards/{fakeId}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        getabank = await ac.get("/banks")
        bankId = getabank.json()[0]["id"]
        bankName = getabank.json()[0]["name"]
        card_data = {"bankId": bankId, "cardType": "TestType", "bankName": bankName, "paymentMethod": "Credito","id":""}
        response = await ac.post("/cards", json=card_data)
    assert response.status_code == 201
    assert response.json()["cardType"] == "TestType"

@pytest.mark.asyncio
async def test_create_card_with_invalid_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        getabank = await ac.get("/banks")
        bankId = getabank.json()[0]["id"]
        bankName = getabank.json()[0]["name"]
        card_data = {"bankId": bankId,"cardType": "TestType", "bankName": "Fake Bank", "paymentMethod": "Credito","id":""}
        response = await ac.post("/cards", json=card_data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_list_cards_by_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        getabank = await ac.get("/banks")
        bankId = getabank.json()[0]["id"]
        bankName = getabank.json()[0]["name"]
        response = await ac.get(f"/cards/by-bank/{bankId}")
    assert response.status_code == 200
    assert response.json()[0]["bankName"] == bankName

@pytest.mark.asyncio
async def test_list_cards_by_unexistent_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.get(f"/cards/by-bank/{fakeId}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        getabank = await ac.get("/banks")
        bankId = getabank.json()[0]["id"]
        bankName = getabank.json()[0]["name"]
        # Crea una tarjeta primero para obtener su id
        card_data = {"bankId": bankId, "cardType": "TestType", "bankName": bankName, "paymentMethod": "Credito","id":""}
        create_response = await ac.post("/cards", json=card_data)
        card_id = create_response.json()["id"]
        print(card_id)

        # Actualiza la tarjeta
        update_data = {"cardType": "TestTypeUpdated","id":card_id, "bankId": bankId, "bankName": bankName, "paymentMethod": "Credito"}
        response = await ac.put(f"/cards/{card_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["cardType"] == "TestTypeUpdated"

@pytest.mark.asyncio
async def test_update_unexistent_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        update_data = {"cardType": "TestTypeUpdated","id":fakeId, "bankId": "668971b39dd5b5392c45edc9", "bankName": "Banco de Chile", "paymentMethod": "Credito"}
        response = await ac.put(f"/cards/{fakeId}", json=update_data)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        getabank = await ac.get("/banks")
        bankId = getabank.json()[0]["id"]
        bankName = getabank.json()[0]["name"]
        # Crea una tarjeta primero para obtener su id
        card_data = {"bankId": bankId, "cardType": "TestType", "bankName": bankName, "paymentMethod": "Credito","id":""}
        create_response = await ac.post("/cards", json=card_data)
        card_id = create_response.json()["id"]

        # Elimina la tarjeta
        response = await ac.delete(f"/cards/{card_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_unexistent_card():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una tarjeta primero para obtener su id
        fakeId = str(ObjectId())
        response = await ac.delete(f"/cards/{fakeId}")
    assert response.status_code == 404
