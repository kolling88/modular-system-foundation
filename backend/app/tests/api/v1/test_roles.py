from fastapi.testclient import TestClient
from app.core.config import settings

def test_create_role(client: TestClient) -> None:
    data = {"name": "manager", "description": "Manager role", "permissions": "read,write,delete"}
    response = client.post(
        f"{settings.API_V1_STR}/roles/", json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content

def test_read_roles(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/roles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_role_by_id(client: TestClient) -> None:
    # Primeiro cria um perfil
    data = {"name": "viewer", "description": "Viewer role"}
    create_res = client.post(f"{settings.API_V1_STR}/roles/", json=data)
    role_id = create_res.json()["id"]
    
    # Depois busca por ID
    response = client.get(f"{settings.API_V1_STR}/roles/{role_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "viewer"
