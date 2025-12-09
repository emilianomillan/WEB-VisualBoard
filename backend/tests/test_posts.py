import pytest
from fastapi import status


def test_get_posts_empty(client):
    """Test: Obtener posts cuando no hay ninguno"""
    response = client.get("/api/posts")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["total_pages"] == 0


def test_create_post_success(client, test_user, test_post_data):
    """Test: Crear un post exitosamente"""
    response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["title"] == test_post_data["title"]
    assert data["description"] == test_post_data["description"]
    assert data["image_url"] == test_post_data["image_url"]
    assert data["user_id"] == test_user
    assert data["tags"] == test_post_data["tags"]
    assert "id" in data
    assert "created_at" in data


def test_create_post_without_user_header(client, test_post_data):
    """Test: Crear post sin header de usuario debe fallar"""
    response = client.post(
        "/api/posts",
        json=test_post_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_posts_with_pagination(client, test_user):
    """Test: Obtener posts con paginación"""
    # Crear varios posts
    for i in range(15):
        client.post(
            "/api/posts",
            json={
                "title": f"Post {i}",
                "image_url": f"https://example.com/image{i}.jpg",
                "tags": [f"tag{i}"]
            },
            headers={"X-User-Id": test_user}
        )
    
    # Obtener primera página
    response = client.get("/api/posts?page=1&per_page=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["total_pages"] == 2
    assert data["page"] == 1
    
    # Obtener segunda página
    response = client.get("/api/posts?page=2&per_page=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 5
    assert data["page"] == 2


def test_get_post_by_id(client, test_user, test_post_data):
    """Test: Obtener un post por ID"""
    # Crear un post
    create_response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    post_id = create_response.json()["id"]
    
    # Obtener el post por ID
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == test_post_data["title"]


def test_get_post_not_found(client):
    """Test: Obtener un post inexistente debe retornar 404"""
    response = client.get("/api/posts/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_post_authorized(client, test_user, test_post_data):
    """Test: Actualizar post siendo el autor"""
    # Crear un post
    create_response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    post_id = create_response.json()["id"]
    
    # Actualizar el post (PUT)
    update_data = {
        "title": "Updated Title",
        "description": "Updated description",
        "image_url": "https://example.com/updated.jpg",
        "tags": ["updated", "test"]
    }
    response = client.put(
        f"/api/posts/{post_id}",
        json=update_data,
        headers={"X-User-Id": test_user}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_update_post_unauthorized(client, test_user, test_post_data):
    """Test: Actualizar post sin ser el autor debe retornar 403"""
    # Crear un post
    create_response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    post_id = create_response.json()["id"]
    
    # Intentar actualizar con otro usuario
    update_data = {
        "title": "Hacked Title",
        "description": "Hacked",
        "image_url": "https://example.com/hacked.jpg",
        "tags": ["hacked"]
    }
    response = client.put(
        f"/api/posts/{post_id}",
        json=update_data,
        headers={"X-User-Id": "another_user"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized" in response.json()["detail"]


def test_patch_post_partial_update(client, test_user, test_post_data):
    """Test: Actualización parcial con PATCH"""
    # Crear un post
    create_response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    post_id = create_response.json()["id"]
    
    # Actualizar solo el título (PATCH)
    patch_data = {"title": "Partially Updated Title"}
    response = client.patch(
        f"/api/posts/{post_id}",
        json=patch_data,
        headers={"X-User-Id": test_user}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == patch_data["title"]
    assert data["description"] == test_post_data["description"]  # Sin cambios
    assert data["image_url"] == test_post_data["image_url"]  # Sin cambios


def test_delete_post_authorized(client, test_user, test_post_data):
    """Test: Eliminar post siendo el autor"""
    # Crear un post
    create_response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    post_id = create_response.json()["id"]
    
    # Eliminar el post
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"X-User-Id": test_user}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verificar que el post fue eliminado
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post_unauthorized(client, test_user, test_post_data):
    """Test: Eliminar post sin ser el autor debe retornar 403"""
    # Crear un post
    create_response = client.post(
        "/api/posts",
        json=test_post_data,
        headers={"X-User-Id": test_user}
    )
    post_id = create_response.json()["id"]
    
    # Intentar eliminar con otro usuario
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"X-User-Id": "another_user"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_filter_posts_by_min_date(client, test_user):
    """Test: Filtrar posts por fecha mínima"""
    # Crear un post
    response = client.post(
        "/api/posts",
        json={
            "title": "Old Post",
            "image_url": "https://example.com/old.jpg"
        },
        headers={"X-User-Id": test_user}
    )
    old_post = response.json()
    
    # Obtener posts con fecha mínima (no debería incluir el post anterior)
    response = client.get(f"/api/posts?min_date=2099-01-01T00:00:00Z")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 0
    
    # Obtener posts con fecha mínima anterior (debería incluir el post)
    response = client.get(f"/api/posts?min_date=2020-01-01T00:00:00Z")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == old_post["id"]


def test_filter_posts_by_user_id(client):
    """Test: Filtrar posts por usuario"""
    # Crear posts de diferentes usuarios
    client.post(
        "/api/posts",
        json={
            "title": "User1 Post",
            "image_url": "https://example.com/user1.jpg"
        },
        headers={"X-User-Id": "user1"}
    )
    
    client.post(
        "/api/posts",
        json={
            "title": "User2 Post",
            "image_url": "https://example.com/user2.jpg"
        },
        headers={"X-User-Id": "user2"}
    )
    
    # Filtrar por user1
    response = client.get("/api/posts?user_id=user1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["user_id"] == "user1"
    
    # Filtrar por user2
    response = client.get("/api/posts?user_id=user2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["user_id"] == "user2"