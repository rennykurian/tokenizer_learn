from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TokenizerMode(StrEnum):
    TIKTOKEN = "tiktoken"
    CUSTOM = "custom"


class TokenStatus(StrEnum):
    NEW = "new"
    EXISTING = "existing"


class TokenizationRequest(BaseModel):
    text: str = Field(min_length=1)
    mode: TokenizerMode
    encoding: str | None = None

    @model_validator(mode="after")
    def validate_encoding_for_mode(self) -> "TokenizationRequest":
        if self.mode is TokenizerMode.TIKTOKEN and not self.encoding:
            raise ValueError("A Tiktoken encoding is required.")
        if self.mode is TokenizerMode.CUSTOM and self.encoding is not None:
            raise ValueError("Custom Tokenizer does not accept an encoding.")
        return self


class TokenResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int = Field(ge=0)
    token_id: int = Field(ge=0)
    text: str
    details: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
    is_new: bool = False


class TokenStatistics(BaseModel):
    character_count: int = Field(ge=0)
    word_count: int = Field(ge=0)
    token_count: int = Field(ge=0)
    tokens_per_word: float = Field(ge=0)
    tokens_per_character: float = Field(ge=0)


class VocabularyEntry(BaseModel):
    token_id: int = Field(ge=0)
    token: str
    frequency: int = Field(ge=0)
    status: TokenStatus


class TokenizationResponse(BaseModel):
    mode: TokenizerMode
    encoding: str | None
    tokens: list[TokenResult]
    statistics: TokenStatistics
    vocabulary: list[VocabularyEntry] = Field(default_factory=list)


class ExtractedDocument(BaseModel):
    text: str
    source_type: str
