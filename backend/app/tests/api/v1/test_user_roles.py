from fastapi.testclient import TestClient
from app.core.config import settings

def test_assign_role_to_user(client: TestClient) -> None:
    # 1. Criar usuário
    user_data = {"email": "role_test@example.com", "password": "pass", "full_name": "Role Test"}
    user_res = client.post(f"{settings.API_V1_STR}/users/", json=user_data)
    user_id = user_res.json()["id"]
    
    # 2. Criar perfil
    role_data = {"name": "editor", "description": "Editor role"}
    role_res = client.post(f"{settings.API_V1_STR}/roles/", json=role_data)
    role_id = role_res.json()["id"]
    
    # 3. Atribuir perfil ao usuário
    assign_res = client.post(f"{settings.API_V1_STR}/users/{user_id}/roles/{role_id}")
    assert assign_res.status_code == 200
    
    # 4. Verificar se o perfil está na lista do usuário
    user_info = client.get(f"{settings.API_V1_STR}/users/{user_id}")
    roles = user_info.json()["roles"]
    assert any(r["id"] == role_id for r in roles)

def test_remove_role_from_user(client: TestClient) -> None:
    # 1. Criar usuário e perfil
    user_res = client.post(f"{settings.API_V1_STR}/users/", json={"email": "del_role@ex.com", "password": "p", "full_name": "N"})
    user_id = user_res.json()["id"]
    role_res = client.post(f"{settings.API_V1_STR}/roles/", json={"name": "temp_role"})
    role_id = role_res.json()["id"]
    
    # 2. Atribuir
    client.post(f"{settings.API_V1_STR}/users/{user_id}/roles/{role_id}")
    
    # 3. Remover
    response = client.delete(f"{settings.API_V1_STR}/users/{user_id}/roles/{role_id}")
    assert response.status_code == 200
    
    # 4. Verificar
    user_info = client.get(f"{settings.API_V1_STR}/users/{user_id}")
    assert not any(r["id"] == role_id for r in user_info.json()["roles"])
