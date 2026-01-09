from fastapi.testclient import TestClient
from app.core.config import settings

def test_create_user(client: TestClient) -> None:
    data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
        "is_superuser": False
    }
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert content["full_name"] == data["full_name"]
    assert "id" in content
    assert "hashed_password" not in content

def test_read_users(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user(client: TestClient) -> None:
    # Criar usuário
    data = {"email": "update@example.com", "password": "pass", "full_name": "Old Name"}
    create_res = client.post(f"{settings.API_V1_STR}/users/", json=data)
    user_id = create_res.json()["id"]
    
    # Atualizar nome
    update_data = {"full_name": "New Name"}
    response = client.put(f"{settings.API_V1_STR}/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Name"
