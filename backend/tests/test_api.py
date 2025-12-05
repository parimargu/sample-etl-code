from fastapi.testclient import TestClient
from app.main import app
from app.services.search_service import SearchService
from app.api.endpoints import get_search_service
from unittest.mock import MagicMock
import pytest

client = TestClient(app)

# Mock SearchService
mock_service = MagicMock(spec=SearchService)

def override_get_search_service():
    return mock_service

app.dependency_overrides[get_search_service] = override_get_search_service

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to NLP Search API"}

def test_search():
    mock_service.search.return_value = [
        {"chunk_id": "1:0", "doc_id": "1", "text": "test", "score": 0.9}
    ]
    
    response = client.post("/api/v1/search", json={"query": "test"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["chunk_id"] == "1:0"

def test_get_document():
    mock_service.get_document.return_value = {"doc_id": "1", "text": "full text"}
    
    response = client.get("/api/v1/document/1")
    assert response.status_code == 200
    assert response.json()["text"] == "full text"

def test_get_document_not_found():
    mock_service.get_document.return_value = None
    
    response = client.get("/api/v1/document/999")
    assert response.status_code == 404
