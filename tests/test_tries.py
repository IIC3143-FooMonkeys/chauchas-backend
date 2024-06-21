import pytest
from httpx import AsyncClient
from main import app  # Asegúrate de que esto apunte al archivo correcto donde inicias tu app FastAPI

@pytest.mark.asyncio
async def test_get_banks():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/banks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_bank():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un banco primero para obtener su id
        bank_data = {"name": "Test Bank"}
        create_response = await ac.post("/banks", json=bank_data)
        bank_id = create_response.json()["id"]

        # Ahora lee el banco
        response = await ac.get(f"/banks/{bank_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Bank"

@pytest.mark.asyncio
async def test_create_bank():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        bank_data = {"name": "Test Bank"}
        response = await ac.post("/banks", json=bank_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Bank"

@pytest.mark.asyncio
async def test_update_bank():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un banco primero para obtener su id
        bank_data = {"name": "Test Bank"}
        create_response = await ac.post("/banks", json=bank_data)
        bank_id = create_response.json()["id"]

        # Actualiza el banco
        update_data = {"name": "Updated Test Bank"}
        response = await ac.put(f"/banks/{bank_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Bank"

@pytest.mark.asyncio
async def test_delete_bank():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un banco primero para obtener su id
        bank_data = {"name": "Test Bank"}
        create_response = await ac.post("/banks", json=bank_data)
        bank_id = create_response.json()["id"]

        # Elimina el banco
        response = await ac.delete(f"/banks/{bank_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_cards():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_card():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea una tarjeta primero para obtener su id
        card_data = {"bankId": "123", "cardType": "Credit", "bankName": "Test Bank", "paymentMethod": "Visa"}
        create_response = await ac.post("/cards", json=card_data)
        card_id = create_response.json()["id"]

        # Ahora lee la tarjeta
        response = await ac.get(f"/cards/{card_id}")
    assert response.status_code == 200
    assert response.json()["cardType"] == "Credit"

@pytest.mark.asyncio
async def test_create_card():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        card_data = {"bankId": "123", "cardType": "Credit", "bankName": "Test Bank", "paymentMethod": "Visa"}
        response = await ac.post("/cards", json=card_data)
    assert response.status_code == 201
    assert response.json()["cardType"] == "Credit"

@pytest.mark.asyncio
async def test_update_card():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea una tarjeta primero para obtener su id
        card_data = {"bankId": "123", "cardType": "Credit", "bankName": "Test Bank", "paymentMethod": "Visa"}
        create_response = await ac.post("/cards", json=card_data)
        card_id = create_response.json()["id"]

        # Actualiza la tarjeta
        update_data = {"bankId": "123", "cardType": "Debit", "bankName": "Test Bank", "paymentMethod": "MasterCard"}
        response = await ac.put(f"/cards/{card_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["cardType"] == "Debit"

@pytest.mark.asyncio
async def test_delete_card():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea una tarjeta primero para obtener su id
        card_data = {"bankId": "123", "cardType": "Credit", "bankName": "Test Bank", "paymentMethod": "Visa"}
        create_response = await ac.post("/cards", json=card_data)
        card_id = create_response.json()["id"]

        # Elimina la tarjeta
        response = await ac.delete(f"/cards/{card_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_categories():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea una categoría primero para obtener su id
        category_data = {"name": "Test Category"}
        create_response = await ac.post("/categories", json=category_data)
        category_id = create_response.json()["id"]

        # Ahora lee la categoría
        response = await ac.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Category"

@pytest.mark.asyncio
async def test_create_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        category_data = {"name": "Test Category"}
        response = await ac.post("/categories", json=category_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Category"

@pytest.mark.asyncio
async def test_update_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea una categoría primero para obtener su id
        category_data = {"name": "Test Category"}
        create_response = await ac.post("/categories", json=category_data)
        category_id = create_response.json()["id"]

        # Actualiza la categoría
        update_data = {"name": "Updated Test Category"}
        response = await ac.put(f"/categories/{category_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Category"

@pytest.mark.asyncio
async def test_delete_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea una categoría primero para obtener su id
        category_data = {"name": "Test Category"}
        create_response = await ac.post("/categories", json=category_data)
        category_id = create_response.json()["id"]

        # Elimina la categoría
        response = await ac.delete(f"/categories/{category_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_discounts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/discounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_discount():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un descuento primero para obtener su id
        discount_data = {
            "url": "http://test.com",
            "local": "Test Local",
            "discount": 20,
            "description": "Test Discount",
            "category": "Test Category",
            "expiration": "2024-12-31T00:00:00",
            "days": "Monday",
            "card": "Test Card",
            "cardType": "Credit",
            "paymentType": "Online",
            "bankName": "Test Bank"
        }
        create_response = await ac.post("/discounts", json=discount_data)
        discount_id = create_response.json()["id"]

        # Ahora lee el descuento
        response = await ac.get(f"/discounts/{discount_id}")
    assert response.status_code == 200
    assert response.json()["description"] == "Test Discount"

@pytest.mark.asyncio
async def test_update_discount():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un descuento primero para obtener su id
        discount_data = {
            "url": "http://test.com",
            "local": "Test Local",
            "discount": 20,
            "description": "Test Discount",
            "category": "Test Category",
            "expiration": "2024-12-31T00:00:00",
            "days": "Monday",
            "card": "Test Card",
            "cardType": "Credit",
            "paymentType": "Online",
            "bankName": "Test Bank"
        }
        create_response = await ac.post("/discounts", json=discount_data)
        discount_id = create_response.json()["id"]

        # Actualiza el descuento
        update_data = {
            "url": "http://updated.com",
            "local": "Updated Local",
            "discount": 30,
            "description": "Updated Discount",
            "category": "Updated Category",
            "expiration": "2024-12-31T00:00:00",
            "days": "Tuesday",
            "card": "Updated Card",
            "cardType": "Debit",
            "paymentType": "Offline",
            "bankName": "Updated Bank"
        }
        response = await ac.put(f"/discounts/{discount_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Discount"

@pytest.mark.asyncio
async def test_delete_discount():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un descuento primero para obtener su id
        discount_data = {
            "url": "http://test.com",
            "local": "Test Local",
            "discount": 20,
            "description": "Test Discount",
            "category": "Test Category",
            "expiration": "2024-12-31T00:00:00",
            "days": "Monday",
            "card": "Test Card",
            "cardType": "Credit",
            "paymentType": "Online",
            "bankName": "Test Bank"
        }
        create_response = await ac.post("/discounts", json=discount_data)
        discount_id = create_response.json()["id"]

        # Elimina el descuento
        response = await ac.delete(f"/discounts/{discount_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un usuario primero para obtener su id
        user_data = {"_id": "123", "auth0Id": "auth0|123", "cards": []}
        create_response = await ac.post("/users", json=user_data)
        user_id = create_response.json()["_id"]

        # Ahora lee el usuario
        response = await ac.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["_id"] == "123"

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_data = {"_id": "123", "auth0Id": "auth0|123", "cards": []}
        response = await ac.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["_id"] == "123"

@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un usuario primero para obtener su id
        user_data = {"_id": "123", "auth0Id": "auth0|123", "cards": []}
        create_response = await ac.post("/users", json=user_data)
        user_id = create_response.json()["_id"]

        # Actualiza el usuario
        update_data = {"_id": "123", "auth0Id": "auth0|456", "cards": []}
        response = await ac.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["auth0Id"] == "auth0|456"

@pytest.mark.asyncio
async def test_add_card_to_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un usuario primero para obtener su id
        user_data = {"_id": "123", "auth0Id": "auth0|123", "cards": []}
        create_response = await ac.post("/users", json=user_data)
        user_id = create_response.json()["_id"]

        # Crea una tarjeta para asociar al usuario
        card_data = {"bankId": "123", "cardType": "Credit", "bankName": "Test Bank", "paymentMethod": "Visa"}
        create_card_response = await ac.post("/cards", json=card_data)
        card_id = create_card_response.json()["id"]

        # Añade la tarjeta al usuario
        response = await ac.put(f"/users/{user_id}/add-card/{card_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_card_from_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crea un usuario primero para obtener su id
        user_data = {"_id": "123", "auth0Id": "auth0|123", "cards": []}
        create_response = await ac.post("/users", json=user_data)
        user_id = create_response.json()["_id"]

        # Crea una tarjeta para asociar al usuario
        card_data = {"bankId": "123", "cardType": "Credit", "bankName": "Test Bank", "paymentMethod": "Visa"}
        create_card_response = await ac.post("/cards", json=card_data)
        card_id = create_card_response.json()["id"]

        # Añade la tarjeta al usuario
        await ac.put(f"/users/{user_id}/add-card/{card_id}")

        # Elimina la tarjeta del usuario
        response = await ac.put(f"/users/{user_id}/delete-card/{card_id}")
    assert response.status_code == 200
