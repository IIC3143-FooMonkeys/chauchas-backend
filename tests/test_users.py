import pytest
from httpx import AsyncClient
from main import app
from bson import ObjectId

URL = "https://www.bozitoapi.online/"
@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_one_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        response = await ac.get(f"/users/{fakeId}")
    assert response.status_code == 200
    assert response.json()["auth0Id"] == fakeId

@pytest.mark.asyncio
async def test_get_one_existent_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        creation_response = await ac.get(f"/users/{fakeId}")
        second_response = await ac.get(f"/users/{fakeId}")
    assert second_response.status_code == 200
    assert second_response.json()["auth0Id"] == fakeId

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        print(fakeId)
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response = await ac.post(f"/users", json=user_data)

    assert creation_response.status_code == 201
    assert creation_response.json()["auth0Id"] == fakeId

@pytest.mark.asyncio
async def test_edit_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        print(fakeId)
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response_1 = await ac.post(f"/users", json=user_data)
        fakeId_2 = str(ObjectId())
        user_data_2 = {"auth0Id": fakeId_2, "cards": []}
        creation_response_2 = await ac.put(f"/users/{fakeId}", json=user_data_2)
    assert creation_response_2.status_code == 200
    assert creation_response_2.json()["auth0Id"] == fakeId_2

@pytest.mark.asyncio
async def test_edit_invalid_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        print(fakeId)
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response_2 = await ac.put(f"/users/{fakeId}", json=user_data)
    assert creation_response_2.status_code == 404

@pytest.mark.asyncio
async def test_look_user_no_cards():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response = await ac.post(f"/users", json=user_data)
        next_response = await ac.get(f"/users/{fakeId}/cards")

    assert next_response.status_code == 404

@pytest.mark.asyncio
async def test_look_user_not_registered():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        next_response = await ac.get(f"/users/{fakeId}/cards")

    assert next_response.status_code == 400

@pytest.mark.asyncio
async def test_look_user_with_cards(): # También testea poner user card
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response = await ac.post(f"/users", json=user_data)
        look_card_response = await ac.get(f"/cards")
        card = look_card_response.json()[0]["id"]
        add_card_response = await ac.put(f"/users/{fakeId}/add-card/{card}")
        next_response = await ac.get(f"/users/{fakeId}/cards")
    assert next_response.status_code == 200

@pytest.mark.asyncio
async def test_look_user_with_cards_and_delete_one():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response = await ac.post(f"/users", json=user_data)
        look_card_response = await ac.get(f"/cards")
        card = look_card_response.json()[0]["id"]
        add_card_response = await ac.put(f"/users/{fakeId}/add-card/{card}")
        delete_card_response = await ac.put(f"/users/{fakeId}/delete-card/{card}")
        next_response = await ac.get(f"/users/{fakeId}/cards")
    assert next_response.status_code == 404

@pytest.mark.asyncio
async def test_add_invalid_card_to_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        fakeId_2 = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response = await ac.post(f"/users", json=user_data)
        add_card_response = await ac.put(f"/users/{fakeId}/add-card/{fakeId_2}")
    assert add_card_response.status_code == 404

@pytest.mark.asyncio
async def test_add_card_to_invalid_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        look_card_response = await ac.get(f"/cards")
        card = look_card_response.json()[0]["id"]
        add_card_response = await ac.put(f"/users/{fakeId}/add-card/{card}")
    assert add_card_response.status_code == 400

@pytest.mark.asyncio
async def test_delete_invalid_card_to_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        fakeId_2 = str(ObjectId())
        user_data = {"auth0Id": fakeId, "cards": []}
        creation_response = await ac.post(f"/users", json=user_data)
        delete_card_response = await ac.put(f"/users/{fakeId}/delete-card/{fakeId_2}")
    assert delete_card_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_card_to_invalid_user():
    async with AsyncClient(app=app, base_url=URL) as ac:
        fakeId = str(ObjectId())
        delete_card_response = await ac.put(f"/users/{fakeId}/delete-card/668971b39dd5b5392c45edd0")
    assert delete_card_response.status_code == 400
