from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── Helpers ──────────────────────────────────────────────
def create_task(title="Test Task", description="Test Description"):
    response = client.post("/tasks", json={"title": title, "description": description})
    return response


# ── Tests ────────────────────────────────────────────────
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running 🚀"}


def test_create_task():
    response = create_task("Buy groceries", "Milk, eggs, bread")
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert not data["completed"]
    assert "id" in data


def test_get_all_tasks():
    create_task("Task A")
    create_task("Task B")
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


def test_get_single_task():
    created = create_task("Single Task")
    task_id = created.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_not_found():
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    created = create_task("Old Title")
    task_id = created.json()["id"]
    response = client.put(
        f"/tasks/{task_id}", json={"title": "New Title", "description": "Updated"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_update_task_not_found():
    response = client.put(
        "/tasks/99999", json={"title": "Ghost Task", "description": "Doesn't exist"}
    )
    assert response.status_code == 404


def test_delete_task():
    created = create_task("To be deleted")
    task_id = created.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}


def test_delete_task_not_found():
    response = client.delete("/tasks/99999")
    assert response.status_code == 404
