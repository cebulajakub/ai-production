import logging

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


async def unhandled_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:

    logger.error(
        "Unhandled exception | method=%s | path=%s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__)
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )