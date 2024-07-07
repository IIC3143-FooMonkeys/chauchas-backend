import pytest
from httpx import AsyncClient
from main import app
from bson import ObjectId
from .admin_info import admin
URL = "https://www.bozitoapi.online/"
@pytest.mark.asyncio
async def test_get_banks():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/banks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea un banco primero para obtener su id
        bank_data = {"name": "Test Bank","id":""}
        create_response = await ac.post(f"/banks?userId={admin}", json=bank_data)
        bank_id = create_response.json()["id"]
        # Ahora lee el banco
        response = await ac.get(f"/banks/{bank_id}")
    assert response.json()["name"] == "Test Bank"

@pytest.mark.asyncio
async def test_read_unexistent_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.get(f"/banks/{fakeId}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        bank_data = {"name": "Test Bank","id":""}
        response = await ac.post(f"/banks?userId={admin}", json=bank_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Bank"

@pytest.mark.asyncio
async def test_update_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        bank_data = {"name": "Test Bank","id":""}
        create_response = await ac.post(f"/banks?userId={admin}", json=bank_data)
        bank_id = create_response.json()["id"]

        # Actualiza el banco
        update_data = {"name": "Updated Test Bank","id":f"{bank_id}"}
        response = await ac.put(f"/banks/{bank_id}?userId={admin}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Bank"

@pytest.mark.asyncio
async def test_update_unexistent_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        # Actualiza el banco
        update_data = {"name": "asd","id":f"123"}
        response = await ac.put(f"/banks/{fakeId}?userId={admin}", json=update_data)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea un banco primero para obtener su id
        bank_data = {"name": "Test Bank","id":""}
        create_response = await ac.post(f"/banks?userId={admin}", json=bank_data)
        bank_id = create_response.json()["id"]

        # Elimina el banco
        response = await ac.delete(f"/banks/{bank_id}?userId={admin}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_unexistent_bank():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.delete(f"/banks/{fakeId}?userId={admin}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_bank_invalid_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        bank_data = {"name": "Test Bank","id":""}
        response = await ac.post(f"/banks?userId={fakeId}", json=bank_data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_bank_unauthorized():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": [], "userType": 0}
        creation_response_1 = await ac.post(f"/users?userId={admin}", json=user_data)
        validUser = creation_response_1.json()["auth0Id"]
        bank_data = {"name": "Test Bank","id":""}
        response = await ac.post(f"/banks?userId={validUser}", json=bank_data)
    assert response.status_code == 403