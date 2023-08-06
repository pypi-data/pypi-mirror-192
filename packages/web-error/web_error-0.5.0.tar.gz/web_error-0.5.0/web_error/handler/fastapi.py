import json
import logging
from typing import List, Optional

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from web_error import constant
from web_error.error import HttpException
from web_error.handler import starlette

logger = logging.getLogger(__name__)


def exception_handler(request: starlette.Request, exc: Exception) -> starlette.JSONResponse:  # noqa: ARG001
    status = constant.SERVER_ERROR
    message = "Unhandled exception occurred."
    response = {
        "message": message,
        "debug_message": str(exc),
        "code": None,
    }

    if isinstance(exc, HTTPException):
        response["message"] = exc.detail
        status = exc.status_code

    if isinstance(exc, RequestValidationError):
        response["message"] = "Request validation error."
        response["debug_message"] = json.loads(exc.json())
        status = 422

    if isinstance(exc, HttpException):
        response = exc.marshal()
        status = exc.status

    if status >= constant.SERVER_ERROR:
        logger.exception(message, exc_info=(type(exc), exc, exc.__traceback__))

    return starlette.JSONResponse(
        status_code=status,
        content=response,
    )


def generate_handler_with_cors(
    allow_origins: Optional[List[str]] = None,
    allow_credentials: bool = True,
    allow_methods: Optional[List[str]] = None,
    allow_headers: Optional[List[str]] = None,
) -> starlette.JSONResponse:
    return starlette.generate_handler_with_cors(
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        _exception_handler=exception_handler,
    )
