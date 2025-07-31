"""Test the custom security exception classes."""

import pytest
from fastapi_secure_errors.exceptions import (
    SecurityHTTPException,
    SecureMethodNotAllowed,
    SecureNotFound,
    SecureForbidden,
    SecureUnauthorized,
    SecureInternalServerError
)


class TestSecurityHTTPException:
    """Test the base SecurityHTTPException class."""
    
    def test_init_basic(self):
        """Test basic initialization."""
        exc = SecurityHTTPException(status_code=400, detail="Test error")
        assert exc.status_code == 400
        assert exc.detail == "Test error"
        assert exc.headers == {}
    
    def test_init_with_headers(self):
        """Test initialization with headers."""
        headers = {"X-Custom": "value"}
        exc = SecurityHTTPException(status_code=500, detail="Server error", headers=headers)
        assert exc.status_code == 500
        assert exc.detail == "Server error"
        assert exc.headers == headers
    
    def test_init_none_headers(self):
        """Test initialization with None headers."""
        exc = SecurityHTTPException(status_code=404, detail="Not found", headers=None)
        assert exc.status_code == 404
        assert exc.detail == "Not found"
        assert exc.headers == {}


class TestSecureMethodNotAllowed:
    """Test the SecureMethodNotAllowed exception."""
    
    def test_default_init(self):
        """Test default initialization."""
        exc = SecureMethodNotAllowed()
        assert exc.status_code == 405
        assert exc.detail == "Method not allowed"
        assert exc.headers == {}
    
    def test_custom_detail(self):
        """Test initialization with custom detail."""
        exc = SecureMethodNotAllowed(detail="Custom method not allowed message")
        assert exc.status_code == 405
        assert exc.detail == "Custom method not allowed message"
        assert exc.headers == {}


class TestSecureNotFound:
    """Test the SecureNotFound exception."""
    
    def test_default_init(self):
        """Test default initialization."""
        exc = SecureNotFound()
        assert exc.status_code == 404
        assert exc.detail == "Resource not found"
        assert exc.headers == {}
    
    def test_custom_detail(self):
        """Test initialization with custom detail."""
        exc = SecureNotFound(detail="Custom not found message")
        assert exc.status_code == 404
        assert exc.detail == "Custom not found message"
        assert exc.headers == {}


class TestSecureForbidden:
    """Test the SecureForbidden exception."""
    
    def test_default_init(self):
        """Test default initialization."""
        exc = SecureForbidden()
        assert exc.status_code == 403
        assert exc.detail == "Access denied"
        assert exc.headers == {}
    
    def test_custom_detail(self):
        """Test initialization with custom detail."""
        exc = SecureForbidden(detail="Custom forbidden message")
        assert exc.status_code == 403
        assert exc.detail == "Custom forbidden message"
        assert exc.headers == {}


class TestSecureUnauthorized:
    """Test the SecureUnauthorized exception."""
    
    def test_default_init(self):
        """Test default initialization."""
        exc = SecureUnauthorized()
        assert exc.status_code == 401
        assert exc.detail == "Authentication required"
        assert exc.headers == {}
    
    def test_custom_detail(self):
        """Test initialization with custom detail."""
        exc = SecureUnauthorized(detail="Custom unauthorized message")
        assert exc.status_code == 401
        assert exc.detail == "Custom unauthorized message"
        assert exc.headers == {}


class TestSecureInternalServerError:
    """Test the SecureInternalServerError exception."""
    
    def test_default_init(self):
        """Test default initialization."""
        exc = SecureInternalServerError()
        assert exc.status_code == 500
        assert exc.detail == "Internal server error"
        assert exc.headers == {}
    
    def test_custom_detail(self):
        """Test initialization with custom detail."""
        exc = SecureInternalServerError(detail="Custom server error message")
        assert exc.status_code == 500
        assert exc.detail == "Custom server error message"
        assert exc.headers == {}


class TestExceptionInheritance:
    """Test that all exceptions inherit from the base classes correctly."""
    
    def test_inheritance_chain(self):
        """Test that all custom exceptions inherit from SecurityHTTPException."""
        exceptions = [
            SecureMethodNotAllowed(),
            SecureNotFound(),
            SecureForbidden(),
            SecureUnauthorized(),
            SecureInternalServerError()
        ]
        
        for exc in exceptions:
            assert isinstance(exc, SecurityHTTPException)
            # SecurityHTTPException inherits from HTTPException
            from fastapi import HTTPException
            assert isinstance(exc, HTTPException)
