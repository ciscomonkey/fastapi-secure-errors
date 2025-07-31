"""Test package imports and public API."""

import pytest


class TestPackageImports:
    """Test that all public components can be imported."""
    
    def test_main_imports(self):
        """Test importing main components from the package."""
        from fastapi_secure_errors import (
            setup_secure_error_handlers,
            SecurityHTTPException,
            SecureMethodNotAllowed,
            SecureNotFound,
            SecureForbidden,
            SecureUnauthorized,
            SecureInternalServerError
        )
        
        # Verify they are all callable/classes
        assert callable(setup_secure_error_handlers)
        assert issubclass(SecurityHTTPException, Exception)
        assert issubclass(SecureMethodNotAllowed, SecurityHTTPException)
        assert issubclass(SecureNotFound, SecurityHTTPException)
        assert issubclass(SecureForbidden, SecurityHTTPException)
        assert issubclass(SecureUnauthorized, SecurityHTTPException)
        assert issubclass(SecureInternalServerError, SecurityHTTPException)
    
    def test_submodule_imports(self):
        """Test importing from submodules."""
        from fastapi_secure_errors.exceptions import (
            SecurityHTTPException,
            SecureMethodNotAllowed,
            SecureNotFound,
            SecureForbidden,
            SecureUnauthorized,
            SecureInternalServerError
        )
        
        from fastapi_secure_errors.handlers import (
            secure_http_exception_handler,
            secure_validation_exception_handler,
            secure_starlette_exception_handler
        )
        
        # Verify handlers are callable
        assert callable(secure_http_exception_handler)
        assert callable(secure_validation_exception_handler)
        assert callable(secure_starlette_exception_handler)
    
    def test_package_all_exports(self):
        """Test that __all__ is properly defined."""
        import fastapi_secure_errors
        
        assert hasattr(fastapi_secure_errors, '__all__')
        all_exports = fastapi_secure_errors.__all__
        
        expected_exports = [
            'setup_secure_error_handlers',
            'SecurityHTTPException',
            'SecureMethodNotAllowed',
            'SecureNotFound',
            'SecureForbidden',
            'SecureUnauthorized',
            'SecureInternalServerError'
        ]
        
        for export in expected_exports:
            assert export in all_exports
            assert hasattr(fastapi_secure_errors, export)
    
    def test_star_import(self):
        """Test that star import works correctly."""
        # This would normally be discouraged, but we test it to ensure __all__ is correct
        namespace = {}
        exec("from fastapi_secure_errors import *", namespace)
        
        expected_in_namespace = [
            'setup_secure_error_handlers',
            'SecurityHTTPException',
            'SecureMethodNotAllowed',
            'SecureNotFound',
            'SecureForbidden',
            'SecureUnauthorized',
            'SecureInternalServerError'
        ]
        
        for name in expected_in_namespace:
            assert name in namespace
    
    def test_no_internal_exports(self):
        """Test that internal modules are not explicitly exported in __all__."""
        import fastapi_secure_errors
        
        # These modules are imported but should not be in __all__
        all_exports = fastapi_secure_errors.__all__
        assert 'handlers' not in all_exports
        assert 'exceptions' not in all_exports
        
        # But the main function and exceptions should be available
        assert hasattr(fastapi_secure_errors, 'setup_secure_error_handlers')
        assert hasattr(fastapi_secure_errors, 'SecurityHTTPException')


class TestPackageMetadata:
    """Test package metadata and structure."""
    
    def test_package_has_version(self):
        """Test that package has version information."""
        try:
            from fastapi_secure_errors import __version__
            assert isinstance(__version__, str)
        except ImportError:
            # If __version__ is not defined, that's also acceptable
            # for simple packages that rely on pyproject.toml
            pass
    
    def test_fastapi_dependency(self):
        """Test that FastAPI is available (required dependency)."""
        import fastapi
        assert hasattr(fastapi, 'FastAPI')
        assert hasattr(fastapi, 'HTTPException')
    
    def test_exception_inheritance_chain(self):
        """Test the complete inheritance chain of custom exceptions."""
        from fastapi_secure_errors import SecurityHTTPException
        from fastapi import HTTPException
        
        # SecurityHTTPException should inherit from FastAPI's HTTPException
        assert issubclass(SecurityHTTPException, HTTPException)
        assert issubclass(SecurityHTTPException, Exception)
        
        # All custom exceptions should inherit from SecurityHTTPException
        from fastapi_secure_errors import (
            SecureMethodNotAllowed,
            SecureNotFound,
            SecureForbidden,
            SecureUnauthorized,
            SecureInternalServerError
        )
        
        custom_exceptions = [
            SecureMethodNotAllowed,
            SecureNotFound,
            SecureForbidden,
            SecureUnauthorized,
            SecureInternalServerError
        ]
        
        for exc_class in custom_exceptions:
            assert issubclass(exc_class, SecurityHTTPException)
            assert issubclass(exc_class, HTTPException)
            assert issubclass(exc_class, Exception)
