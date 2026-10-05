from app.schemas.tokenization import TokenResult, VocabularyEntry
from app.services.vocabulary_service import VocabularyService


class CustomTokenizer:
    def __init__(self, vocabulary: VocabularyService) -> None:
        self.vocabulary = vocabulary

    @staticmethod
    def split(text: str) -> list[str]:
        tokens: list[str] = []
        current: list[str] = []
        for character in text:
            if character.isalnum():
                current.append(character)
                continue
            if current:
                tokens.append("".join(current))
                current.clear()
            if not character.isspace():
                tokens.append(character)
        if current:
            tokens.append("".join(current))
        return tokens

    def tokenize(self, text: str) -> "CustomTokenization":
        parts = self.split(text)
        assignments, vocabulary = self.vocabulary.assign(parts)
        tokens = [
            TokenResult(index=index, token_id=item.token_id, text=part, is_new=item.is_new)
            for index, (part, item) in enumerate(zip(parts, assignments, strict=True))
        ]
        return CustomTokenization(tokens=tokens, vocabulary=vocabulary)


class CustomTokenization:
    def __init__(self, tokens: list[TokenResult], vocabulary: list[VocabularyEntry]) -> None:
        self.tokens = tokens
        self.vocabulary = vocabulary
