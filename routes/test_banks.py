import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
from routes.main import router  # Importa el enrutador principal desde routes.main

client = TestClient(app)

@pytest.fixture
def setup_database():
    # Simulamos una base de datos en memoria para pruebas
    from config.database import banksTable
    
    # Limpia la tabla de bancos antes de las pruebas
    banksTable.delete_many({})

    # Inserta algunos datos de prueba
    banksTable.insert_many([
        {'_id': ObjectId('60d6b0c33e0a26004874c2d6'), 'name': 'Bank A'},
        {'_id': ObjectId('60d6b0c33e0a26004874c2d7'), 'name': 'Bank B'},
    ])

    yield

    # Limpiar la base de datos después de las pruebas
    banksTable.delete_many({})

def test_get_banks(setup_database):
    response = client.get("/banks")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Verifica que haya dos bancos en la respuesta

def test_get_bank_by_id(setup_database):
    # Obtenemos el ID de uno de los bancos insertados en setup_database
    bank_id = '60d6b0c33e0a26004874c2d6'  # ID del primer banco en nuestra lista de prueba

    response = client.get(f"/banks/{bank_id}")
    assert response.status_code == 200
    assert response.json()['name'] == 'Bank A'

def test_get_bank_by_id_not_found(setup_database):
    # Utilizamos un ID que no existe en la base de datos
    bank_id = '60d6b0c33e0a26004874c2d8'  # ID ficticio que no existe

    response = client.get(f"/banks/{bank_id}")
    assert response.status_code == 404

def test_create_bank():
    new_bank = {
        'name': 'New Bank'
    }

    response = client.post("/banks", json=new_bank)
    assert response.status_code == 201
    assert response.json()['name'] == 'New Bank'

def test_update_bank(setup_database):
    bank_id = '60d6b0c33e0a26004874c2d6'  # ID del primer banco en nuestra lista de prueba
    updated_bank = {
        'name': 'Updated Bank'
    }

    response = client.put(f"/banks/{bank_id}", json=updated_bank)
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated Bank'

def test_update_bank_not_found():
    bank_id = '60d6b0c33e0a26004874c2d8'  # ID ficticio que no existe
    updated_bank = {
        'name': 'Updated Bank'
    }

    response = client.put(f"/banks/{bank_id}", json=updated_bank)
    assert response.status_code == 404

def test_delete_bank(setup_database):
    bank_id = '60d6b0c33e0a26004874c2d6'  # ID del primer banco en nuestra lista de prueba

    response = client.delete(f"/banks/{bank_id}")
    assert response.status_code == 200
    assert response.json()['name'] == 'Bank A'

def test_delete_bank_not_found():
    bank_id = '60d6b0c33e0a26004874c2d8'  # ID ficticio que no existe

    response = client.delete(f"/banks/{bank_id}")
    assert response.status_code == 404
