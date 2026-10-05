from app.services.custom_tokenizer import CustomTokenizer
from app.services.vocabulary_service import VocabularyService


def test_custom_split_groups_unicode_alphanumeric_and_emits_punctuation():
    assert CustomTokenizer.split("Hi, 世界! 42") == ["Hi", ",", "世界", "!", "42"]


def test_vocabulary_assigns_deterministic_ids_and_updates_frequency():
    vocabulary = VocabularyService()
    tokenizer = CustomTokenizer(vocabulary)

    first = tokenizer.tokenize("hello hello world")
    second = tokenizer.tokenize("world hello")

    assert [token.token_id for token in first.tokens] == [0, 0, 1]
    assert [token.token_id for token in second.tokens] == [1, 0]
    assert {entry.token: entry.frequency for entry in second.vocabulary} == {
        "hello": 3,
        "world": 2,
    }
    assert [token.is_new for token in second.tokens] == [False, False]


def test_vocabulary_reset_restores_initial_ids():
    vocabulary = VocabularyService()
    tokenizer = CustomTokenizer(vocabulary)
    tokenizer.tokenize("old")

    vocabulary.reset()

    assert tokenizer.tokenize("new").tokens[0].token_id == 0
