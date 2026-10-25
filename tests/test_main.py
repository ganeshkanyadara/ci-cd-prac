import sys
from pathlib import Path

# Add repository root to sys.path so main can be imported regardless of execution context
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import main
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_tasks():
    # Give every test a clean, independent task list.
    main.tasks.clear()
    main.next_id = 1
    yield
    main.tasks.clear()
    main.next_id = 1


client = TestClient(main.app)


def test_get_empty_tasks():
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    response = client.post(
        "/api/tasks",
        json={"title": "Learn FastAPI"}
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    }


def test_reject_empty_task():
    response = client.post(
        "/api/tasks",
        json={"title": "   "}
    )

    assert response.status_code == 400


def test_complete_task():
    created = client.post(
        "/api/tasks",
        json={"title": "Learn GitHub Actions"}
    )

    task_id = created.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task():
    created = client.post(
        "/api/tasks",
        json={"title": "Temporary task"}
    )

    task_id = created.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204
    assert client.get("/api/tasks").json() == []


def test_update_missing_task():
    response = client.patch(
        "/api/tasks/999",
        json={"completed": True}
    )

    assert response.status_code == 404
