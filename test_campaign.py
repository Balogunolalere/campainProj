from fastapi.testclient import TestClient
from main import app
from app.utils import generate_unique_id

client = TestClient(app)


def test_create_campaign():
    # First, create a campaign
    campaign_data = {
        "key": generate_unique_id(),  # Add a key to the campaign data to avoid conflicts with other tests
        "subject": "Test Create Campaign",
        "content": "Test Content",
        "list_ids": ["list1", "list2"],
        "status": "draft"
    }
    response = client.post("/campaign/", json=campaign_data)
    assert response.status_code == 200

    # Then, try to create a campaign with the same subject
    response = client.post("/campaign/", json=campaign_data)
    assert response.status_code == 400

def test_update_campaign():
    # First, create a campaign
    campaign_data = {
        "key": generate_unique_id(),  # Add a key to the campaign data to avoid conflicts with other tests
        "subject": "Test Campaign",
        "content": "Test Content",
        "list_ids": ["list1", "list2"],
        "status": "scheduled"
    }
    response = client.post("/campaign/", json=campaign_data)
    assert response.status_code == 200
    campaign_key = response.json()["key"]

    # Then, update the campaign
    update_data = {
        "subject": "Updated Test Campaign",
        "content": "Updated Test Content",
        "status": "sent"
    }
    response = client.patch(f"/campaign/{campaign_key}", json=update_data)
    assert response.status_code == 200

    # Finally, check if the update was successful
    response = client.get(f"/campaign/{campaign_key}")
    assert response.status_code == 200
    assert response.json()["subject"] == "Updated Test Campaign"
    assert response.json()["content"] == "Updated Test Content"
    assert response.json()["status"] == "sent"
