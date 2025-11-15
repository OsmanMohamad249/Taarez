"""
Tests for Template CRUD endpoints.

Run with: pytest backend/tests/test_templates.py
"""

from fastapi.testclient import TestClient
from backend.main import app
import time


def test_template_crud_flow(client: TestClient):
    # Create a template
    name = f"test_template_{int(time.time()*1000)}"
    payload = {"components": [{"type": "text", "value": "Hello"}]}

    create_resp = client.post(
        "/api/v1/templates/",
        json={
            "name": name,
            "description": "A test template",
            "payload": payload,
        },
    )

    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == name
    tmpl_id = created["id"]

    # Listing should include the created template
    list_resp = client.get("/api/v1/templates/")
    assert list_resp.status_code == 200
    templates = list_resp.json()
    assert any(t["id"] == tmpl_id for t in templates)

    # Get by id
    get_resp = client.get(f"/api/v1/templates/{tmpl_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == tmpl_id
    assert data["payload"] == payload

    # Update template
    new_name = name + "_v2"
    updated_payload = {"components": [{"type": "text", "value": "World"}]}
    update_resp = client.put(
        f"/api/v1/templates/{tmpl_id}",
        json={
            "name": new_name,
            "description": "Updated",
            "payload": updated_payload,
        },
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["name"] == new_name
    assert updated["payload"] == updated_payload

    # Creating another template with same name should fail
    dup_resp = client.post(
        "/api/v1/templates/",
        json={"name": new_name, "payload": {}},
    )
    assert dup_resp.status_code == 400

    # Delete template
    del_resp = client.delete(f"/api/v1/templates/{tmpl_id}")
    assert del_resp.status_code == 200

    # Now fetching should return 404
    not_found = client.get(f"/api/v1/templates/{tmpl_id}")
    assert not_found.status_code == 404
