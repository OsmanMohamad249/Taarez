"""
Tests for user authentication system requirements.

Tests verify:
1. New users created via POST /users/ have customer role by default
2. Users can login via POST /login/access-token
3. GET /users/me returns user data including role

Note: These tests require a running database.
Run with: pytest tests/test_user_roles.py
"""

import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_user_registration_defaults_to_customer():
    """Test that new users created via POST /users/ have CUSTOMER role by default."""
    email = f"customer_{int(time.time())}@example.com"
    password = "testpass123"

    # Register new user via POST /users/
    response = client.post(
        "/api/v1/users/",
        json={
            "email": email,
            "password": password,
            "first_name": "Test",
            "last_name": "Customer",
        },
    )

    assert response.status_code == 201
    data = response.json()

    # Verify user was created
    assert data["email"] == email
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Customer"

    # Verify role is CUSTOMER
    assert data["role"] == "customer"
    assert data["is_active"] is True
    assert data["is_superuser"] is False


def test_user_can_login():
    """Test that a user can login via POST /login/access-token."""
    email = f"login_{int(time.time())}@example.com"
    password = "testpass123"

    # First register a user
    client.post(
        "/api/v1/users/",
        json={
            "email": email,
            "password": password,
            "first_name": "Login",
            "last_name": "Test",
        },
    )

    # Now test login via POST /login/access-token
    response = client.post(
        "/api/v1/login/access-token",
        data={
            "username": email,  # OAuth2 uses 'username' field for email
            "password": password,
        },
    )

    assert response.status_code == 200
    data = response.json()

    # Verify token response
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_users_me_returns_role():
    """Test that GET /users/me returns user data including role."""
    email = f"me_{int(time.time())}@example.com"
    password = "testpass123"

    # Register a new user
    client.post(
        "/api/v1/users/",
        json={
            "email": email,
            "password": password,
            "first_name": "Me",
            "last_name": "Test",
        },
    )

    # Login to get access token
    login_response = client.post(
        "/api/v1/login/access-token",
        data={"username": email, "password": password},
    )
    token = login_response.json()["access_token"]

    # Get current user via GET /users/me
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # Verify all user data is returned
    assert data["email"] == email
    assert data["first_name"] == "Me"
    assert data["last_name"] == "Test"
    assert data["is_active"] is True
    assert data["is_superuser"] is False

    # Verify role is included and is CUSTOMER
    assert "role" in data
    assert data["role"] == "customer"


def test_login_wrong_credentials():
    """Test that login fails with wrong credentials."""
    response = client.post(
        "/api/v1/login/access-token",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_users_me_without_token():
    """Test that GET /users/me fails without authentication."""
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401


def test_users_me_with_invalid_token():
    """Test that GET /users/me fails with invalid token."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token_here"},
    )

    assert response.status_code == 401


def test_duplicate_email_registration():
    """Test that registering with duplicate email fails."""
    email = f"duplicate_{int(time.time())}@example.com"
    user_data = {
        "email": email,
        "password": "testpass123",
        "first_name": "Duplicate",
        "last_name": "Test",
    }

    # First registration
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201

    # Second registration with same email
    response2 = client.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()
