from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_text_tokenization_returns_tokens_and_statistics():
    response = client.post(
        "/api/v1/tokenize",
        json={"text": "hello world", "mode": "tiktoken", "encoding": "cl100k_base"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert [token["token_id"] for token in payload["tokens"]] == [15339, 1917]
    assert payload["statistics"]["token_count"] == 2


def test_text_tokenization_rejects_whitespace_only_input():
    response = client.post(
        "/api/v1/tokenize",
        json={"text": "  \n", "mode": "custom"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_INPUT"


def test_text_tokenization_rejects_empty_input_with_standard_error():
    response = client.post(
        "/api/v1/tokenize",
        json={"text": "", "mode": "custom"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_INPUT"


def test_encoding_list_is_available():
    response = client.get("/api/v1/encodings")

    assert response.status_code == 200
    assert "cl100k_base" in response.json()


def test_text_tokenization_rejects_unsupported_encoding():
    response = client.post(
        "/api/v1/tokenize",
        json={"text": "hello", "mode": "tiktoken", "encoding": "invalid"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "UNSUPPORTED_ENCODING"
