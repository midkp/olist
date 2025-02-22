"""Tests for the CSV upload routes."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Add test functions as needed
def test_upload_customers():
    """Test uploading a CSV to the customers endpoint."""
    with open("test_data.csv", "rb") as f:
        response = client.post(
            "/api/v1/upload/customers",
            files={"file": ("test_data.csv", f, "text/csv")},
        )
    assert response.status_code == 200
