from app.services.tiktoken_service import TiktokenService


def test_tiktoken_uses_selected_encoding_and_returns_real_ids():
    service = TiktokenService()

    tokens = service.tokenize("hello world", "cl100k_base")

    assert [token.token_id for token in tokens] == [15339, 1917]
    assert "byte_length" in tokens[0].details
    assert "token_bytes_hex" in tokens[0].details


def test_tiktoken_results_are_repeatable_and_encodings_are_supported():
    service = TiktokenService()

    first = service.tokenize("hello", "cl100k_base")
    second = service.tokenize("hello", "cl100k_base")

    assert service.list_encodings()
    assert first == second
