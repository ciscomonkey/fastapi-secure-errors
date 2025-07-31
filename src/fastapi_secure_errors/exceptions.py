from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional

class SecurityHTTPException(HTTPException):
    """Base class for security-focused HTTP exceptions"""
    
    def __init__(self, status_code: int, detail: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers or {}

class SecureMethodNotAllowed(SecurityHTTPException):
    """405 without exposing allowed methods"""
    def __init__(self, detail: str = "Method not allowed"):
        super().__init__(status_code=405, detail=detail)

class SecureNotFound(SecurityHTTPException):
    """404 with generic message"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)

class SecureForbidden(SecurityHTTPException):
    """403 without exposing resource existence"""
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status_code=403, detail=detail)

class SecureUnauthorized(SecurityHTTPException):
    """401 with minimal information"""
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(status_code=401, detail=detail)

class SecureInternalServerError(SecurityHTTPException):
    """500 without exposing internal details"""
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=500, detail=detail)