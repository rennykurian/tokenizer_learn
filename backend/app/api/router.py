from fastapi import APIRouter

from app.api.routes.files import router as files_router
from app.api.routes.tokenization import router as tokenization_router
from app.api.routes.vocabulary import router as vocabulary_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(tokenization_router, tags=["tokenization"])
api_router.include_router(files_router, tags=["files"])
api_router.include_router(vocabulary_router, tags=["vocabulary"])
