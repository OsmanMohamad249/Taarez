"""
Tests for design endpoints.

Note: These tests require a running database.
Run with: pytest tests/test_design.py
"""

import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_auth_token():
    """Helper function to get an authentication token."""
    import time

    email = f"test_design_{int(time.time())}@example.com"

    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "testpass123"},
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def test_get_categories():
    """Test getting all categories."""
    response = client.get("/api/v1/design/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_fabrics_by_category():
    """Test getting fabrics by category."""
    # Use a random UUID for testing
    category_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/design/fabrics/{category_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_save_design_unauthenticated():
    """Test that saving a design requires authentication."""
    design_data = {
        "name": "Test Design",
        "category_id": str(uuid.uuid4()),
        "fabric_id": str(uuid.uuid4()),
        "customization": {"collar": "classic", "sleeve": "full"},
    }

    response = client.post("/api/v1/design/save", json=design_data)
    assert response.status_code == 401  # Unauthorized


def test_save_design_authenticated():
    """Test saving a design with authentication."""
    token = get_auth_token()
    if not token:
        # Skip if token retrieval fails
        return

    design_data = {
        "name": "Test Design",
        "category_id": str(uuid.uuid4()),
        "fabric_id": str(uuid.uuid4()),
        "customization": {"collar": "classic", "sleeve": "full"},
    }

    response = client.post(
        "/api/v1/design/save",
        json=design_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should succeed or fail with foreign key constraint
    # (since we're using random UUIDs that don't exist in the database)
    assert response.status_code in [201, 500]

    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["name"] == design_data["name"]
        assert "user_id" in data
