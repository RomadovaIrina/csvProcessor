from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_mime_type():
    response = client.post(
        "/csv-processor/",
        files={"file": ("test.txt", "Erron, invalid type", "text/plain")}
    )
    assert response.status_code == 415
    assert response.json() == {"detail": "Invalid file type. Supported types: csv"}


