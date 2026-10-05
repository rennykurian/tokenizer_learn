from app.schemas.tokenization import TokenStatistics


def calculate_statistics(text: str, token_count: int) -> TokenStatistics:
    character_count = len(text)
    word_count = len(text.split())
    return TokenStatistics(
        character_count=character_count,
        word_count=word_count,
        token_count=token_count,
        tokens_per_word=round(token_count / word_count, 4) if word_count else 0.0,
        tokens_per_character=round(token_count / character_count, 4) if character_count else 0.0,
    )
