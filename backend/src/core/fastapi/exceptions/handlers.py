from fastapi import status, Request, Response, FastAPI, HTTPException
from fastapi.exceptions import (
    RequestValidationError,
    StarletteHTTPException,
    ResponseValidationError,
)
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse


def init_error_handlers(app: FastAPI, admin_email: str):
    """Declare the handlers to catch different types of exceptions."""

    @app.exception_handler(Exception)
    async def internal_server_error_handler(req: Request, exc: Exception):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return JSONResponse(
            status_code=status_code,
            content={
                "status": status_code,
                "type": type(exc).__name__,
                "description": f'An internal error has occurred. Contact the system administrator at "{admin_email}"',
                "details": str(exc),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        req: Request, exc: RequestValidationError
    ):
        status_code = status.HTTP_400_BAD_REQUEST

        return JSONResponse(
            status_code=status_code,
            content={
                "status": status_code,
                "type": type(exc).__name__,
                "details": {"message": str(exc), "errors": exc.errors()},
            },
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_error_handler(
        res: Response, exc: ResponseValidationError
    ):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        return JSONResponse(
            status_code=status_code,
            content={
                "status": status_code,
                "type": type(exc).__name__,
                "details": {"message": str(exc), "errors": exc.errors()},
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(req: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "type": type(exc).__name__,
                "details": {"message": exc.detail},
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        req: Request, exc: StarletteHTTPException
    ):
        if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return await internal_server_error_handler(req, exc)

        return PlainTextResponse(status_code=exc.status_code)
