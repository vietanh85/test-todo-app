import pytest
import os
from fastapi.testclient import TestClient

# Set environment variable before importing app to use in-memory DB
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app import app
from database import db

@pytest.fixture
def client():
    # Use TestClient as context manager to trigger lifespan (startup/shutdown)
    with TestClient(app) as client:
        yield client

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_route_ordering_bug(client):
    """
    Regression test: /todos/completed was matching /todos/{id} and failing validation
    because 'completed' is not an integer.
    """
    response = client.get("/todos/completed")
    # If the bug exists, this would be 422 (Validation Error)
    # If fixed, it should be 200 (Empty list)
    assert response.status_code == 200
    assert response.json() == []

def test_workflow(client):
    # 1. Create Todo
    response = client.post("/todos", json={"title": "Test Task", "description": "Test Desc"})
    assert response.status_code == 201
    data = response.json()
    todo_id = data["id"]
    assert data["title"] == "Test Task"
    assert data["completed"] is False

    # 2. Update to completed
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # 3. Check /todos/completed
    response = client.get("/todos/completed")
    assert response.status_code == 200
    completed_list = response.json()
    assert len(completed_list) == 1
    assert completed_list[0]["id"] == todo_id

    # 4. Check /todos/active
    response = client.get("/todos/active")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # 5. Delete
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    
    # 6. Verify gone
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
