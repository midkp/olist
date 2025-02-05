from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_csv_upload():
    with open("test_data.csv", "rb") as f:
        response = client.post(
            "/api/v1/upload/customers",
            files={"file": ("test_data.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    assert response.json()["status"] == "success"