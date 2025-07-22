from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_products_with_auth():
    # 1) Register a test user
    register_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    client.post("/users/register", json=register_data)

    # 2) Log in to get a token
    login_data = {
        "username": "testuser@example.com",
        "password": "testpassword"
    }
    login_resp = client.post("/users/login", data=login_data)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # 3) Call /products/ with Authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get("/products/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
