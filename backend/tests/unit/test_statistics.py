from app.services.statistics_service import calculate_statistics


def test_statistics_count_unicode_whitespace_words_and_ratios():
    result = calculate_statistics("hé llo\n世界", token_count=3)

    assert result.character_count == 9
    assert result.word_count == 3
    assert result.token_count == 3
    assert result.tokens_per_word == 1.0
    assert result.tokens_per_character == 0.3333


def test_statistics_zero_denominator_is_safe():
    result = calculate_statistics("", token_count=0)

    assert result.tokens_per_word == 0
    assert result.tokens_per_character == 0
