"""
Test health endpoint
"""
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app('testing')
    with app.test_client() as client:
        yield client


@pytest.fixture
def app():
    """Create test app"""
    app = create_app('testing')
    yield app


def test_health_endpoint_exists(client):
    """Test that /health endpoint exists"""
    response = client.get('/health')
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """Test that /health returns JSON"""
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_health_endpoint_returns_ok_status(client):
    """Test that /health returns status ok"""
    response = client.get('/health')
    data = response.get_json()
    assert data is not None
    assert 'status' in data
    assert data['status'] == 'ok'


def test_app_can_be_imported():
    """Test that app can be imported and created"""
    app = create_app('testing')
    assert app is not None
    assert app.config['TESTING'] is True
