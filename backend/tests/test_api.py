from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_list_paper() -> None:
    client = TestClient(app)
    payload = {
        "title": "A review of catalytic pathways",
        "doi": "10.1000/example",
        "year": 2024,
        "tags": ["catalysis", "review"],
    }

    create_resp = client.post("/api/papers", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["title"] == payload["title"]

    list_resp = client.get("/api/papers")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(item["id"] == created["id"] for item in items)
