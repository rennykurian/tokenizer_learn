from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title="Tokenizer Application API", version="1.0.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type"],
    )
    application.include_router(api_router)

    @application.exception_handler(HTTPException)
    async def http_error_handler(request: Request, error: HTTPException) -> JSONResponse:
        detail = error.detail
        if isinstance(detail, dict) and "code" in detail and "message" in detail:
            payload = {"error": detail}
        else:
            payload = {"error": {"code": "REQUEST_FAILED", "message": str(detail)}}
        return JSONResponse(status_code=error.status_code, content=payload, headers=error.headers)

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, error: RequestValidationError
    ) -> JSONResponse:
        payload = {
            "error": {
                "code": "INVALID_INPUT",
                "message": "Check the submitted input and try again.",
            }
        }
        return JSONResponse(status_code=422, content=payload)

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
