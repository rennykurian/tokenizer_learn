from app.services.vocabulary_service import VocabularyService


def test_vocabulary_tracks_first_seen_ids_frequency_and_operation_status():
    vocabulary = VocabularyService()
    first_tokens, first_snapshot = vocabulary.assign(["alpha", "alpha", "beta"])

    assert [item.token_id for item in first_tokens] == [0, 0, 1]
    assert all(item.is_new for item in first_tokens)
    assert [(item.token, item.frequency, item.status.value) for item in first_snapshot] == [
        ("alpha", 2, "new"),
        ("beta", 1, "new"),
    ]

    later_tokens, later_snapshot = vocabulary.assign(["beta", "gamma"])
    assert [(item.token_id, item.is_new) for item in later_tokens] == [(1, False), (2, True)]
    assert [(item.token, item.frequency, item.status.value) for item in later_snapshot] == [
        ("alpha", 2, "existing"),
        ("beta", 2, "existing"),
        ("gamma", 1, "new"),
    ]


def test_vocabulary_reset_restarts_ids():
    vocabulary = VocabularyService()
    vocabulary.assign(["before"])
    assert vocabulary.reset() == []
    tokens, _ = vocabulary.assign(["after"])
    assert tokens[0].token_id == 0
