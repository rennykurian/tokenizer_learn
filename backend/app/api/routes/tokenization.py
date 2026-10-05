from fastapi import APIRouter, HTTPException

from app.schemas.errors import ApiError, ApiErrorEnvelope
from app.schemas.tokenization import TokenizationRequest, TokenizationResponse
from app.services.tokenizer_registry import registry

router = APIRouter()


@router.get("/encodings", response_model=list[str])
def list_encodings() -> list[str]:
    return registry.tiktoken.list_encodings()


@router.post(
    "/tokenize",
    response_model=TokenizationResponse,
    responses={400: {"model": ApiErrorEnvelope}},
)
def tokenize(request: TokenizationRequest) -> TokenizationResponse:
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail=ApiError(
                code="INVALID_INPUT", message="Enter non-whitespace text to tokenize."
            ).model_dump(),
        )
    try:
        return TokenizationResponse.model_validate(
            registry.tokenize(request.text, request.mode, request.encoding)
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=ApiError(
                code="UNSUPPORTED_ENCODING", message="Choose a supported encoding."
            ).model_dump(),
        ) from error
