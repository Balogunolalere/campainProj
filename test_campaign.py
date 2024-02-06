from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_campaign_by_key():
    key = "273b01f7-872d-4251-a4ab-d577114a7f47"  # replace with a valid key
    response = client.get(f"/campaign/{key}")
    assert response.status_code == 200
