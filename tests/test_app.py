import os
import sys
from fastapi.testclient import TestClient

# Ensure `src` is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Expect dictionary of activities
    assert isinstance(data, dict)
    assert "Soccer Team" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "test_user@example.com"

    # Ensure email is not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    before = resp.json()
    participants_before = before[activity]["participants"].copy()
    if test_email in participants_before:
        # If by chance it's present, remove it first to ensure a clean slate
        client.post(f"/activities/{activity}/unregister?email={test_email}")

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify present
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert test_email in data[activity]["participants"]

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert test_email not in data[activity]["participants"]
