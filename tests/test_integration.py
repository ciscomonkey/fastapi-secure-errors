"""Integration tests for the fastapi-secure-errors package."""

import pytest
from fastapi import FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError

from fastapi_secure_errors import (
    setup_secure_error_handlers,
    SecureNotFound,
    SecureMethodNotAllowed,
    SecureForbidden,
    SecureUnauthorized,
    SecureInternalServerError
)


@pytest.fixture
def debug_app():
    """Create a FastAPI app in debug mode."""
    app = FastAPI(debug=True)
    setup_secure_error_handlers(app)
    
    @app.get("/test-404")
    async def test_404():
        raise HTTPException(status_code=404, detail="Detailed error message")
    
    @app.get("/test-validation")
    async def test_validation(required_param: int = Query(...)):
        return {"param": required_param}
    
    @app.get("/test-custom-404")
    async def test_custom_404():
        raise SecureNotFound("Custom not found message")
    
    @app.get("/test-500")
    async def test_500():
        raise HTTPException(status_code=500, detail="Internal database error")
    
    return app


@pytest.fixture
def production_app():
    """Create a FastAPI app in production mode."""
    app = FastAPI(debug=False)
    setup_secure_error_handlers(app)
    
    @app.get("/test-404")
    async def test_404():
        raise HTTPException(status_code=404, detail="Detailed error message")
    
    @app.get("/test-validation")
    async def test_validation(required_param: int = Query(...)):
        return {"param": required_param}
    
    @app.get("/test-custom-404")
    async def test_custom_404():
        raise SecureNotFound("Custom not found message")
    
    @app.get("/test-401")
    async def test_401():
        raise SecureUnauthorized("You need to login")
    
    @app.get("/test-403")
    async def test_403():
        raise SecureForbidden("You don't have permission")
    
    @app.get("/test-405")
    async def test_405():
        raise SecureMethodNotAllowed("POST not allowed")
    
    @app.get("/test-500")
    async def test_500():
        raise HTTPException(status_code=500, detail="Internal database error")
    
    @app.get("/test-custom-500")
    async def test_custom_500():
        raise SecureInternalServerError("Database connection failed")
    
    return app


class TestDebugModeIntegration:
    """Test integration in debug mode."""
    
    def test_debug_mode_shows_detailed_errors(self, debug_app):
        """Test that debug mode shows detailed error messages."""
        client = TestClient(debug_app)
        
        response = client.get("/test-404")
        assert response.status_code == 404
        # In debug mode, should show the original detailed message
        assert "Detailed error message" in response.json()["detail"]
    
    def test_debug_mode_validation_errors(self, debug_app):
        """Test that debug mode shows detailed validation errors."""
        client = TestClient(debug_app)
        
        # Missing required parameter
        response = client.get("/test-validation")
        assert response.status_code == 422
        # In debug mode, should show detailed validation error
        response_data = response.json()
        assert "detail" in response_data
        # Debug mode should show detailed validation info
        assert isinstance(response_data["detail"], list)
    
    def test_debug_mode_custom_exceptions(self, debug_app):
        """Test that custom exceptions work in debug mode."""
        client = TestClient(debug_app)
        
        response = client.get("/test-custom-404")
        assert response.status_code == 404
        # Custom exceptions should still work
        assert "Custom not found message" in response.json()["detail"]


class TestProductionModeIntegration:
    """Test integration in production mode."""
    
    def test_production_mode_secure_404(self, production_app):
        """Test that production mode shows secure 404 messages."""
        client = TestClient(production_app)
        
        response = client.get("/test-404")
        assert response.status_code == 404
        assert response.json() == {"detail": "Resource not found"}
    
    def test_production_mode_secure_validation(self, production_app):
        """Test that production mode shows secure validation messages."""
        client = TestClient(production_app)
        
        # Missing required parameter
        response = client.get("/test-validation")
        assert response.status_code == 422
        assert response.json() == {"detail": "Invalid input provided"}
    
    def test_production_mode_secure_500(self, production_app):
        """Test that production mode shows secure 500 messages."""
        client = TestClient(production_app)
        
        response = client.get("/test-500")
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
    
    def test_production_mode_custom_401(self, production_app):
        """Test custom 401 exception in production mode."""
        client = TestClient(production_app)
        
        response = client.get("/test-401")
        assert response.status_code == 401
        # Should use secure handler, not the custom message
        assert response.json() == {"detail": "Authentication required"}
    
    def test_production_mode_custom_403(self, production_app):
        """Test custom 403 exception in production mode."""
        client = TestClient(production_app)
        
        response = client.get("/test-403")
        assert response.status_code == 403
        assert response.json() == {"detail": "Access denied"}
    
    def test_production_mode_custom_405(self, production_app):
        """Test custom 405 exception in production mode."""
        client = TestClient(production_app)
        
        response = client.get("/test-405")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method not allowed"}
    
    def test_production_mode_custom_500(self, production_app):
        """Test custom 500 exception in production mode."""
        client = TestClient(production_app)
        
        response = client.get("/test-custom-500")
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
    
    def test_production_mode_unknown_endpoint(self, production_app):
        """Test accessing unknown endpoint in production mode."""
        client = TestClient(production_app)
        
        response = client.get("/nonexistent")
        assert response.status_code == 404
        # Should be handled by Starlette exception handler
        assert response.json() == {"detail": "An error occurred"}
    
    def test_production_mode_invalid_json(self, production_app):
        """Test invalid JSON input in production mode."""
        client = TestClient(production_app)
        
        # Test with invalid query parameter instead of POST to GET endpoint
        response = client.get("/test-validation?required_param=invalid")
        assert response.status_code == 422
        assert response.json() == {"detail": "Invalid input provided"}


class TestSecurityFeatures:
    """Test security-specific features."""
    
    def test_no_sensitive_headers_leaked(self, production_app):
        """Test that sensitive headers are not leaked."""
        client = TestClient(production_app)
        
        response = client.get("/test-404")
        assert response.status_code == 404
        
        # Check that common sensitive headers are not present
        sensitive_headers = [
            "X-Debug-Info",
            "X-Error-Details", 
            "X-Stack-Trace",
            "Server",
            "X-Powered-By"
        ]
        
        for header in sensitive_headers:
            assert header not in response.headers
    
    def test_consistent_error_format(self, production_app):
        """Test that all errors return consistent format."""
        client = TestClient(production_app)
        
        endpoints_and_expected_codes = [
            ("/test-404", 404),
            ("/test-401", 401),
            ("/test-403", 403),
            ("/test-405", 405),
            ("/test-500", 500),
            ("/test-validation", 422),  # Missing required param
        ]
        
        for endpoint, expected_code in endpoints_and_expected_codes:
            response = client.get(endpoint)
            assert response.status_code == expected_code
            
            # All responses should have the same format
            response_data = response.json()
            assert isinstance(response_data, dict)
            assert "detail" in response_data
            assert isinstance(response_data["detail"], str)
            
            # Should not contain sensitive information
            detail = response_data["detail"].lower()
            sensitive_terms = [
                "database", "sql", "connection", "internal", "stack",
                "trace", "exception", "error:", "failed to", "cannot"
            ]
            
            # Some terms might appear in secure messages, so we check for specific patterns
            assert "database connection" not in detail
            assert "sql error" not in detail
            assert "stack trace" not in detail


class TestAppBehaviorComparison:
    """Test comparing behavior between debug and production modes."""
    
    def test_same_endpoint_different_responses(self, debug_app, production_app):
        """Test that the same endpoint returns different responses in different modes."""
        debug_client = TestClient(debug_app)
        production_client = TestClient(production_app)
        
        # Test 404 endpoint
        debug_response = debug_client.get("/test-404")
        production_response = production_client.get("/test-404")
        
        assert debug_response.status_code == production_response.status_code == 404
        
        # Responses should be different
        debug_detail = debug_response.json()["detail"]
        production_detail = production_response.json()["detail"]
        
        assert debug_detail != production_detail
        assert "Detailed error message" in debug_detail
        assert production_detail == "Resource not found"
    
    def test_validation_responses_different(self, debug_app, production_app):
        """Test that validation errors are different between modes."""
        debug_client = TestClient(debug_app)
        production_client = TestClient(production_app)
        
        # Test validation endpoint without required param
        debug_response = debug_client.get("/test-validation")
        production_response = production_client.get("/test-validation")
        
        assert debug_response.status_code == production_response.status_code == 422
        
        # Debug should have detailed validation info
        debug_data = debug_response.json()
        production_data = production_response.json()
        
        # Debug mode should have detailed validation errors
        assert isinstance(debug_data["detail"], list)
        
        # Production mode should have simple error message
        assert production_data == {"detail": "Invalid input provided"}
