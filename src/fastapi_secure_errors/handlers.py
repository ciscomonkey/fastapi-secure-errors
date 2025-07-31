from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

async def secure_http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with security best practices"""
    
    # Remove sensitive headers
    safe_headers = {}
    
    # Custom responses for specific status codes
    secure_responses = {
        400: {"detail": "Bad request"},
        401: {"detail": "Authentication required"},
        403: {"detail": "Access denied"},
        404: {"detail": "Resource not found"},
        405: {"detail": "Method not allowed"},
        422: {"detail": "Invalid input"},
        429: {"detail": "Too many requests"},
        500: {"detail": "Internal server error"},
        502: {"detail": "Service unavailable"},
        503: {"detail": "Service unavailable"},
    }
    
    # Log the actual error for debugging (server-side only)
    logger.warning(f"HTTP {exc.status_code} on {request.url}: {exc.detail}")
    
    # Return generic message or custom secure message
    response_content = secure_responses.get(
        exc.status_code, 
        {"detail": "An error occurred"}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
        headers=safe_headers
    )

async def secure_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors without exposing internal structure"""
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input provided"}
    )

async def secure_starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle Starlette HTTP exceptions"""
    logger.warning(f"Starlette HTTP {exc.status_code} on {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": "An error occurred"}
    )