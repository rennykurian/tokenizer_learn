from fastapi import APIRouter

from app.schemas.vocabulary import VocabularyEntry
from app.services.tokenizer_registry import registry

router = APIRouter()


@router.get("/vocabulary", response_model=list[VocabularyEntry])
def get_vocabulary() -> list[VocabularyEntry]:
    return registry.vocabulary.snapshot()


@router.delete("/vocabulary", response_model=list[VocabularyEntry])
def reset_vocabulary() -> list[VocabularyEntry]:
    return registry.vocabulary.reset()
