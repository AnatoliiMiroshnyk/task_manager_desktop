"""Integration tests for the FastAPI endpoints."""


def task_payload(title="Prepare release", **overrides):
    payload = {
        "title": title,
        "description": "Create changelog and release notes",
        "status": "todo",
        "priority": "high",
        "due_date": "2030-01-15",
    }
    payload.update(overrides)
    return payload


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_full_crud_flow(client):
    created = client.post("/api/v1/tasks", json=task_payload())
    assert created.status_code == 201
    task_id = created.json()["id"]

    listed = client.get("/api/v1/tasks")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "in_progress", "priority": "medium"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"

    deleted = client.delete(f"/api/v1/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/tasks/{task_id}").status_code == 404


def test_search_filter_and_summary(client):
    client.post("/api/v1/tasks", json=task_payload("Write API tests"))
    client.post("/api/v1/tasks", json=task_payload("Design dashboard", status="done"))

    search = client.get("/api/v1/tasks", params={"search": "API"})
    assert len(search.json()) == 1

    done = client.get("/api/v1/tasks", params={"status": "done"})
    assert len(done.json()) == 1

    summary = client.get("/api/v1/tasks/summary").json()
    assert summary["total"] == 2
    assert summary["todo"] == 1
    assert summary["done"] == 1


def test_rejects_invalid_payload(client):
    response = client.post("/api/v1/tasks", json={"title": ""})
    assert response.status_code == 422
