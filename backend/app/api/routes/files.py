from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.errors import ApiError
from app.schemas.tokenization import ExtractedDocument
from app.services.document_extraction import extract_document
from app.services.file_validation import FileProcessingError

router = APIRouter()


@router.post("/files/extract", response_model=ExtractedDocument)
async def extract_file(file: UploadFile = File(...)) -> ExtractedDocument:
    try:
        return await extract_document(file)
    except FileProcessingError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=ApiError(code=error.code, message=str(error)).model_dump(),
        ) from error
