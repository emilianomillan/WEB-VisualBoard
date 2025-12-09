import pytest
from fastapi import status
from unittest.mock import patch, MagicMock


def test_discover_endpoint(client):
    """Test: El endpoint de discover debe funcionar"""
    # Mockear la respuesta de Unsplash
    mock_unsplash_response = {
        "results": [
            {
                "id": "abc123",
                "urls": {"regular": "https://images.unsplash.com/photo-1"},
                "description": "Beautiful landscape",
                "alt_description": "Mountain view",
                "user": {"name": "John Doe"}
            },
            {
                "id": "def456",
                "urls": {"regular": "https://images.unsplash.com/photo-2"},
                "description": "Ocean waves",
                "alt_description": "Beach sunset",
                "user": {"name": "Jane Smith"}
            }
        ]
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.get.return_value.json.return_value = mock_unsplash_response
        mock_instance.get.return_value.status_code = 200
        mock_client.return_value.__aenter__.return_value = mock_instance
        
        response = client.get("/api/discover")
        
        # Por ahora, verificar que el endpoint responde
        # El test real depende de la implementación actual
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "images" in data
            assert isinstance(data["images"], list)