import pytest
from fastapi import status


def test_health_endpoint(client):
    """Test: El endpoint de health debe funcionar correctamente"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "services" in data
    
    # Verificar servicios
    services = data["services"]
    assert "database" in services
    assert "unsplash" in services  # Cambiado de unsplash_api a unsplash
    
    # El status general debe estar presente
    assert data["status"] in ["healthy", "degraded", "unhealthy"]