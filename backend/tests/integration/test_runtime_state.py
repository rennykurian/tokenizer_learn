from fastapi.testclient import TestClient

from app.main import app
from app.services.tokenizer_registry import TokenizerRegistry, registry

client = TestClient(app)


def test_custom_vocabulary_is_empty_after_runtime_reinitialization():
    registry.vocabulary.reset()
    client.post("/api/v1/tokenize", json={"text": "runtime token", "mode": "custom"})
    assert client.get("/api/v1/vocabulary").json()

    restarted_runtime = TokenizerRegistry()
    assert restarted_runtime.vocabulary.snapshot() == []


def test_health_endpoint_does_not_restore_user_input():
    response = client.get("/health")

    assert response.status_code == 200
    assert "text" not in response.json()
