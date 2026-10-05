from fastapi.testclient import TestClient

from app.main import app
from app.services.tokenizer_registry import registry

client = TestClient(app)


def test_vocabulary_snapshot_and_reset():
    registry.vocabulary.reset()
    client.post("/api/v1/tokenize", json={"text": "new new", "mode": "custom"})

    snapshot = client.get("/api/v1/vocabulary")
    assert snapshot.status_code == 200
    assert snapshot.json()[0]["frequency"] == 2

    reset = client.delete("/api/v1/vocabulary")
    assert reset.status_code == 200
    assert reset.json() == []


def test_tiktoken_does_not_modify_custom_vocabulary():
    registry.vocabulary.reset()
    client.post("/api/v1/tokenize", json={"text": "customword", "mode": "custom"})
    before = client.get("/api/v1/vocabulary").json()
    client.post(
        "/api/v1/tokenize",
        json={"text": "hello", "mode": "tiktoken", "encoding": "cl100k_base"},
    )
    assert client.get("/api/v1/vocabulary").json() == before
