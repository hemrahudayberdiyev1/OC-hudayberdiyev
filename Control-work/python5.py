from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_factorial_api():
    response = client.get("/factorials/factorials/5")
    assert response.status_code == 200
    assert response.json() == [1, 2, 6, 24, 120]

def test_deduplication_api():
    response = client.post("/deduplicate/deduplicate", json={"items": [1,2,2,3]})
    assert response.status_code == 200
    assert response.json() == [1,2,3]

def test_linked_list_api():
    response = client.post("/linked-list/reverse", json={"items": [1,2,3,4]})
    assert response.status_code == 200
    assert response.json() == [4,3,2,1]
