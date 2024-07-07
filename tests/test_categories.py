import pytest
from httpx import AsyncClient
from main import app
from bson import ObjectId
from .admin_info import admin
URL = "https://www.bozitoapi.online/"
@pytest.mark.asyncio
async def test_get_categories():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una categoria
        category_data = {"name":"TestCategory","id":""}
        create_response = await ac.post(f"/categories?userId={admin}", json=category_data)
        category_id = create_response.json()["id"]

        # Ahora lee la tarjeta
        response = await ac.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestCategory"

@pytest.mark.asyncio
async def test_read_unexistent_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())

        # Ahora lee la tarjeta
        response = await ac.get(f"/categories/{fakeId}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una categoria
        category_data = {"name":"TestCategory","id":""}
        response = await ac.post(f"/categories?userId={admin}", json=category_data)
    assert response.status_code == 201
    assert response.json()["name"] == "TestCategory"

@pytest.mark.asyncio
async def test_update_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una categoria
        category_data = {"name":"TestCategory","id":""}
        create_response = await ac.post(f"/categories?userId={admin}", json=category_data)
        category_id = create_response.json()["id"]

        # Actualiza la tarjeta
        update_data = {"name":"TestCategoryUpdated","id":category_id}
        response = await ac.put(f"/categories/{category_id}?userId={admin}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "TestCategoryUpdated"

@pytest.mark.asyncio
async def test_update_unexistent_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        update_data = {"name": "TestCategoryUpdated", "id": fakeId}
        response = await ac.put(f"/categories/{fakeId}?userId={admin}", json=update_data)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una categoria
        category_data = {"name":"TestCategory","id":""}
        create_response = await ac.post(f"/categories?userId={admin}", json=category_data)
        category_id = create_response.json()["id"]

        response = await ac.delete(f"/categories/{category_id}?userId={admin}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_unexistent_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.delete(f"/categories/{fakeId}?userId={admin}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_category():
    async with AsyncClient(app=app, base_url=URL) as ac:
        # Crea una categoria
        category_data = {"name":"TestCategory","id":""}
        response = await ac.post(f"/categories?userId={admin}", json=category_data)
    assert response.status_code == 201
    assert response.json()["name"] == "TestCategory"

@pytest.mark.asyncio
async def test_create_category_invalid_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        # Crea una categoria
        category_data = {"name":"TestCategory","id":""}
        response = await ac.post(f"/categories?userId={fakeId}", json=category_data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_category_unauthorized():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": [], "userType": 0}
        creation_response_1 = await ac.post(f"/users?userId={admin}", json=user_data)
        validUser = creation_response_1.json()["auth0Id"]
        # Crea una categoria
        category_data = {"name": "TestCategory", "id": ""}
        response = await ac.post(f"/categories?userId={validUser}", json=category_data)
    assert response.status_code == 403