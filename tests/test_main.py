"""Tests for the main application."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Add test functions as needed
def test_app_startup():
    """Test that the app starts correctly."""
    response = client.get("/")  # Adjust endpoint as per your API
    assert response.status_code in [200, 404]  # Depending on root endpoint behavior
