import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from models import URL


client = TestClient(app)

@pytest.fixture
def mocked_db_session():
    with patch('main.get_db') as mock_get_db:
        yield mock_get_db.return_value

def test_shorten_url_success(mocked_db_session):
    with patch('utils.generate_short_url') as mock_generate_short_url:
        # Mocking the generate_short_url function to return a dummy URL object
        mock_generate_short_url.return_value = URL(long_url="https://example.com", short_path="abc123")
        
        # Make a POST request to /shorten/ endpoint
        response = client.post("/shorten/", json={"url": "https://example.com"})
        
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "long_url": "https://example.com",
            "short_path": "abc123"
        }
        
        # Ensure that the create_url function was called with the correct arguments
        mocked_db_session.assert_called_once()

def test_shorten_url_invalid_url():
    # Make a POST request to /shorten/ endpoint with an invalid URL
    response = client.post("/shorten/", json={"url": "invalid_url"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid URL"}

