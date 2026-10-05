from app.schemas.tokenization import TokenizerMode
from app.services.custom_tokenizer import CustomTokenizer
from app.services.statistics_service import calculate_statistics
from app.services.tiktoken_service import TiktokenService
from app.services.vocabulary_service import VocabularyService


class TokenizerRegistry:
    def __init__(self) -> None:
        self.vocabulary = VocabularyService()
        self.custom = CustomTokenizer(self.vocabulary)
        self.tiktoken = TiktokenService()

    def tokenize(self, text: str, mode: TokenizerMode, encoding: str | None):
        if mode is TokenizerMode.TIKTOKEN:
            if encoding is None:
                raise ValueError("A Tiktoken encoding is required.")
            tokens = self.tiktoken.tokenize(text, encoding)
            vocabulary = []
        else:
            custom_result = self.custom.tokenize(text)
            tokens = custom_result.tokens
            vocabulary = custom_result.vocabulary
        return {
            "mode": mode,
            "encoding": encoding if mode is TokenizerMode.TIKTOKEN else None,
            "tokens": tokens,
            "statistics": calculate_statistics(text, len(tokens)),
            "vocabulary": vocabulary,
        }


registry = TokenizerRegistry()
