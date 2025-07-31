"""Test the setup_secure_error_handlers function."""

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_secure_errors import setup_secure_error_handlers
from fastapi_secure_errors.exceptions import SecurityHTTPException
from fastapi_secure_errors.handlers import (
    secure_http_exception_handler,
    secure_validation_exception_handler,
    secure_starlette_exception_handler
)


class TestSetupSecureErrorHandlers:
    """Test the setup_secure_error_handlers function."""
    
    def test_setup_in_debug_mode_explicit(self):
        """Test setup when debug=True is explicitly passed."""
        app = FastAPI()
        
        # Store initial exception handlers count
        initial_handlers_count = len(app.exception_handlers)
        
        setup_secure_error_handlers(app, debug=True)
        
        # In debug mode, no new handlers should be added
        assert len(app.exception_handlers) == initial_handlers_count
    
    def test_setup_in_production_mode_explicit(self):
        """Test setup when debug=False is explicitly passed."""
        app = FastAPI()
        
        setup_secure_error_handlers(app, debug=False)
        
        # Should have added 4 exception handlers
        expected_handlers = {
            HTTPException: secure_http_exception_handler,
            RequestValidationError: secure_validation_exception_handler,
            StarletteHTTPException: secure_starlette_exception_handler,
            SecurityHTTPException: secure_http_exception_handler
        }
        
        for exc_type, handler in expected_handlers.items():
            assert exc_type in app.exception_handlers
            assert app.exception_handlers[exc_type] == handler
    
    def test_setup_auto_detect_debug_true(self):
        """Test setup when app.debug=True and debug=None (auto-detect)."""
        app = FastAPI(debug=True)
        
        initial_handlers_count = len(app.exception_handlers)
        
        setup_secure_error_handlers(app)  # debug=None, should auto-detect
        
        # Should detect debug=True and not add handlers
        assert len(app.exception_handlers) == initial_handlers_count
    
    def test_setup_auto_detect_debug_false(self):
        """Test setup when app.debug=False and debug=None (auto-detect)."""
        app = FastAPI(debug=False)
        
        setup_secure_error_handlers(app)  # debug=None, should auto-detect
        
        # Should detect debug=False and add secure handlers
        expected_handlers = {
            HTTPException: secure_http_exception_handler,
            RequestValidationError: secure_validation_exception_handler,
            StarletteHTTPException: secure_starlette_exception_handler,
            SecurityHTTPException: secure_http_exception_handler
        }
        
        for exc_type, handler in expected_handlers.items():
            assert exc_type in app.exception_handlers
            assert app.exception_handlers[exc_type] == handler
    
    def test_setup_auto_detect_no_debug_attribute(self):
        """Test setup when app has no debug attribute."""
        app = FastAPI()
        # Remove debug attribute if it exists
        if hasattr(app, 'debug'):
            delattr(app, 'debug')
        
        setup_secure_error_handlers(app)  # debug=None, should default to False
        
        # Should default to debug=False and add secure handlers
        expected_handlers = {
            HTTPException: secure_http_exception_handler,
            RequestValidationError: secure_validation_exception_handler,
            StarletteHTTPException: secure_starlette_exception_handler,
            SecurityHTTPException: secure_http_exception_handler
        }
        
        for exc_type, handler in expected_handlers.items():
            assert exc_type in app.exception_handlers
            assert app.exception_handlers[exc_type] == handler
    
    def test_multiple_setups_debug_mode(self):
        """Test that multiple setups in debug mode don't cause issues."""
        app = FastAPI(debug=True)
        
        initial_handlers_count = len(app.exception_handlers)
        
        # Call setup multiple times
        setup_secure_error_handlers(app, debug=True)
        setup_secure_error_handlers(app, debug=True)
        setup_secure_error_handlers(app, debug=True)
        
        # Should still have the same number of handlers
        assert len(app.exception_handlers) == initial_handlers_count
    
    def test_multiple_setups_production_mode(self):
        """Test that multiple setups in production mode overwrite handlers."""
        app = FastAPI(debug=False)
        
        # Call setup multiple times
        setup_secure_error_handlers(app, debug=False)
        first_setup_count = len(app.exception_handlers)
        
        setup_secure_error_handlers(app, debug=False)
        second_setup_count = len(app.exception_handlers)
        
        # Should have the same handlers (overwritten, not duplicated)
        assert first_setup_count == second_setup_count
        
        # Verify handlers are still correct
        expected_handlers = {
            HTTPException: secure_http_exception_handler,
            RequestValidationError: secure_validation_exception_handler,
            StarletteHTTPException: secure_starlette_exception_handler,
            SecurityHTTPException: secure_http_exception_handler
        }
        
        for exc_type, handler in expected_handlers.items():
            assert exc_type in app.exception_handlers
            assert app.exception_handlers[exc_type] == handler
    
    def test_switch_from_debug_to_production(self):
        """Test switching from debug to production mode."""
        app = FastAPI()
        
        # First setup in debug mode
        setup_secure_error_handlers(app, debug=True)
        debug_handlers_count = len(app.exception_handlers)
        
        # Then setup in production mode
        setup_secure_error_handlers(app, debug=False)
        
        # Should now have the secure handlers
        assert len(app.exception_handlers) > debug_handlers_count
        
        expected_handlers = {
            HTTPException: secure_http_exception_handler,
            RequestValidationError: secure_validation_exception_handler,
            StarletteHTTPException: secure_starlette_exception_handler,
            SecurityHTTPException: secure_http_exception_handler
        }
        
        for exc_type, handler in expected_handlers.items():
            assert exc_type in app.exception_handlers
            assert app.exception_handlers[exc_type] == handler
    
    def test_switch_from_production_to_debug(self):
        """Test switching from production to debug mode."""
        app = FastAPI()
        
        # First setup in production mode
        setup_secure_error_handlers(app, debug=False)
        production_handlers = dict(app.exception_handlers)
        
        # Then setup in debug mode
        setup_secure_error_handlers(app, debug=True)
        
        # Debug mode should not remove existing handlers
        # (FastAPI doesn't provide a clean way to remove handlers)
        # So the handlers should still be there
        for exc_type, handler in production_handlers.items():
            assert exc_type in app.exception_handlers
