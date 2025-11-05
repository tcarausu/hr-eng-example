from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_add_order_success():
    response = client.post("/orders", json={
        "name": "O-9999",
        "source": "A",
        "target": "D"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "O-9999"

def test_add_order_duplicate():
    client.post("/orders", json={
        "name": "O-8888",
        "source": "A",
        "target": "D"
    })
    response = client.post("/orders", json={
        "name": "O-8888",
        "source": "A",
        "target": "D"
    })
    assert response.status_code == 409

def test_add_order_invalid_nodes():
    response = client.post("/orders", json={
        "name": "O-7777",
        "source": "X",
        "target": "Y"
    })
    assert response.status_code == 400
