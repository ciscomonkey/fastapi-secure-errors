"""Test the secure error handlers."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from fastapi_secure_errors.handlers import (
    secure_http_exception_handler,
    secure_validation_exception_handler,
    secure_starlette_exception_handler
)


@pytest.fixture
def mock_request():
    """Create a mock request for testing."""
    request = MagicMock(spec=Request)
    request.url = "http://example.com/test"
    return request


class TestSecureHttpExceptionHandler:
    """Test the secure HTTP exception handler."""
    
    @pytest.mark.asyncio
    async def test_404_exception(self, mock_request):
        """Test handling of 404 exception."""
        exc = HTTPException(status_code=404, detail="Original detailed message")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 404
        assert response.body == b'{"detail":"Resource not found"}'
    
    @pytest.mark.asyncio
    async def test_401_exception(self, mock_request):
        """Test handling of 401 exception."""
        exc = HTTPException(status_code=401, detail="Invalid credentials provided")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 401
        assert response.body == b'{"detail":"Authentication required"}'
    
    @pytest.mark.asyncio
    async def test_403_exception(self, mock_request):
        """Test handling of 403 exception."""
        exc = HTTPException(status_code=403, detail="You don't have permission")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 403
        assert response.body == b'{"detail":"Access denied"}'
    
    @pytest.mark.asyncio
    async def test_405_exception(self, mock_request):
        """Test handling of 405 exception."""
        exc = HTTPException(status_code=405, detail="GET method not allowed")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 405
        assert response.body == b'{"detail":"Method not allowed"}'
    
    @pytest.mark.asyncio
    async def test_422_exception(self, mock_request):
        """Test handling of 422 exception."""
        exc = HTTPException(status_code=422, detail="Validation failed for field X")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 422
        assert response.body == b'{"detail":"Invalid input"}'
    
    @pytest.mark.asyncio
    async def test_500_exception(self, mock_request):
        """Test handling of 500 exception."""
        exc = HTTPException(status_code=500, detail="Database connection failed")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        assert response.body == b'{"detail":"Internal server error"}'
    
    @pytest.mark.asyncio
    async def test_unknown_status_code(self, mock_request):
        """Test handling of unknown status codes."""
        exc = HTTPException(status_code=418, detail="I'm a teapot")
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 418
        assert response.body == b'{"detail":"An error occurred"}'
    
    @pytest.mark.asyncio
    async def test_exception_with_headers(self, mock_request):
        """Test that headers are not passed through (security)."""
        exc = HTTPException(
            status_code=400, 
            detail="Bad request",
            headers={"X-Sensitive": "secret-info"}
        )
        
        response = await secure_http_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 400
        assert "X-Sensitive" not in response.headers
        # JSONResponse always includes content-type and content-length headers
        # We just care that sensitive headers are not passed through
        assert "content-type" in response.headers
        assert response.headers["content-type"] == "application/json"


class TestSecureValidationExceptionHandler:
    """Test the secure validation exception handler."""
    
    @pytest.mark.asyncio
    async def test_validation_exception(self, mock_request):
        """Test handling of validation exception."""
        # Create a mock validation error
        exc = RequestValidationError([
            {
                "loc": ["query", "param"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ])
        
        response = await secure_validation_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 422
        assert response.body == b'{"detail":"Invalid input provided"}'
    
    @pytest.mark.asyncio
    async def test_multiple_validation_errors(self, mock_request):
        """Test handling of multiple validation errors."""
        exc = RequestValidationError([
            {
                "loc": ["query", "param1"],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": ["body", "field2"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt"
            }
        ])
        
        response = await secure_validation_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 422
        assert response.body == b'{"detail":"Invalid input provided"}'


class TestSecureStarletteExceptionHandler:
    """Test the secure Starlette exception handler."""
    
    @pytest.mark.asyncio
    async def test_starlette_404_exception(self, mock_request):
        """Test handling of Starlette 404 exception."""
        exc = StarletteHTTPException(status_code=404, detail="Page not found")
        
        response = await secure_starlette_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 404
        assert response.body == b'{"detail":"An error occurred"}'
    
    @pytest.mark.asyncio
    async def test_starlette_500_exception(self, mock_request):
        """Test handling of Starlette 500 exception."""
        exc = StarletteHTTPException(status_code=500, detail="Internal error")
        
        response = await secure_starlette_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 500
        assert response.body == b'{"detail":"An error occurred"}'
    
    @pytest.mark.asyncio
    async def test_starlette_custom_status(self, mock_request):
        """Test handling of Starlette custom status code."""
        exc = StarletteHTTPException(status_code=503, detail="Service unavailable")
        
        response = await secure_starlette_exception_handler(mock_request, exc)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 503
        assert response.body == b'{"detail":"An error occurred"}'
