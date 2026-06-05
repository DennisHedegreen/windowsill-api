from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        field = ".".join(str(x) for x in e["loc"] if x != "query")
        errors.append({"field": field, "error": e["msg"]})
    return JSONResponse(status_code=422, content={
        "error": "invalid_parameters",
        "message": "One or more query parameters are invalid.",
        "details": errors,
    })


def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={
        "error": "not_found",
        "message": str(exc.detail) if hasattr(exc, "detail") else "Resource not found.",
    })


def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={
        "error": "server_error",
        "message": "An unexpected error occurred.",
    })
