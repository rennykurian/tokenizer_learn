import pytest
from pydantic import ValidationError

from app.schemas.errors import ApiError, ApiErrorEnvelope
from app.schemas.tokenization import (
    TokenizationRequest,
    TokenizationResponse,
    TokenizerMode,
)


def test_tokenization_request_accepts_supported_modes_and_optional_encoding():
    request = TokenizationRequest(text="hello", mode=TokenizerMode.TIKTOKEN, encoding="cl100k_base")

    assert request.mode is TokenizerMode.TIKTOKEN
    assert request.encoding == "cl100k_base"


def test_tokenization_response_serializes_ordered_tokens_and_statistics():
    response = TokenizationResponse.model_validate(
        {
            "mode": "custom",
            "encoding": None,
            "tokens": [{"index": 0, "token_id": 0, "text": "hello", "details": {}, "is_new": True}],
            "statistics": {
                "character_count": 5,
                "word_count": 1,
                "token_count": 1,
                "tokens_per_word": 1.0,
                "tokens_per_character": 0.2,
            },
            "vocabulary": [{"token_id": 0, "token": "hello", "frequency": 1, "status": "new"}],
        }
    )

    assert response.tokens[0].index == 0
    assert response.vocabulary[0].status == "new"


def test_request_rejects_unknown_mode():
    with pytest.raises(ValidationError):
        TokenizationRequest(text="hello", mode="other")


def test_api_error_uses_stable_envelope():
    payload = ApiErrorEnvelope(error=ApiError(code="INVALID_INPUT", message="Enter text."))

    assert payload.model_dump() == {"error": {"code": "INVALID_INPUT", "message": "Enter text."}}
