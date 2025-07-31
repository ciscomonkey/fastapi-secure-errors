from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .handlers import (
    secure_http_exception_handler,
    secure_validation_exception_handler,
    secure_starlette_exception_handler
)
from .exceptions import (
    SecurityHTTPException,
    SecureMethodNotAllowed,
    SecureNotFound,
    SecureForbidden,
    SecureUnauthorized,
    SecureInternalServerError
)

def setup_secure_error_handlers(app: FastAPI, debug: bool = None):
    """Setup secure error handlers for the FastAPI app
    
    Args:
        app: The FastAPI application instance
        debug: If True, use default FastAPI error handlers. If False, use secure handlers.
               If None (default), auto-detect from app.debug setting.
    """
    # Auto-detect debug mode if not explicitly provided
    if debug is None:
        debug = getattr(app, 'debug', False)
    
    # In debug mode, use default FastAPI error handling for better development experience
    if debug:
        # Don't add custom handlers - let FastAPI use its default handlers
        # which provide detailed error information for debugging
        return
    
    # In production/non-debug mode, use secure error handlers
    # Handle FastAPI HTTP exceptions
    app.add_exception_handler(HTTPException, secure_http_exception_handler)
    
    # Handle validation errors
    app.add_exception_handler(RequestValidationError, secure_validation_exception_handler)
    
    # Handle Starlette HTTP exceptions
    app.add_exception_handler(StarletteHTTPException, secure_starlette_exception_handler)
    
    # Handle custom security exceptions
    app.add_exception_handler(SecurityHTTPException, secure_http_exception_handler)

__all__ = [
    'setup_secure_error_handlers',
    'SecurityHTTPException',
    'SecureMethodNotAllowed',
    'SecureNotFound',
    'SecureForbidden',
    'SecureUnauthorized',
    'SecureInternalServerError'
]