from app.schemas.tokenization import TokenizerMode
from app.services.tokenizer_registry import TokenizerRegistry


def test_custom_vocabulary_changes_do_not_change_tiktoken_results():
    registry = TokenizerRegistry()
    expected = registry.tokenize("hello world", TokenizerMode.TIKTOKEN, "cl100k_base")
    registry.tokenize("custom only", TokenizerMode.CUSTOM, None)
    actual = registry.tokenize("hello world", TokenizerMode.TIKTOKEN, "cl100k_base")

    assert [token.token_id for token in actual["tokens"]] == [
        token.token_id for token in expected["tokens"]
    ]
    assert actual["tokens"] == expected["tokens"]


def test_tiktoken_does_not_change_custom_vocabulary():
    registry = TokenizerRegistry()
    registry.tokenize("custom only", TokenizerMode.CUSTOM, None)
    before = registry.vocabulary.snapshot()
    registry.tokenize("hello world", TokenizerMode.TIKTOKEN, "cl100k_base")

    assert registry.vocabulary.snapshot() == before
