# Testing fastapi-secure-errors

This directory contains comprehensive tests for the `fastapi-secure-errors` package.

## Test Structure

The test suite is organized into the following modules:

### `test_exceptions.py`
Tests for custom exception classes:
- `SecurityHTTPException` - Base security exception
- `SecureMethodNotAllowed` - 405 errors
- `SecureNotFound` - 404 errors  
- `SecureForbidden` - 403 errors
- `SecureUnauthorized` - 401 errors
- `SecureInternalServerError` - 500 errors

### `test_handlers.py`
Tests for secure error handlers:
- `secure_http_exception_handler` - Handles FastAPI HTTP exceptions
- `secure_validation_exception_handler` - Handles validation errors
- `secure_starlette_exception_handler` - Handles Starlette HTTP exceptions

### `test_setup.py`
Tests for the main setup function:
- `setup_secure_error_handlers` - Main configuration function
- Debug vs production mode detection
- Auto-detection of app debug settings
- Multiple setup scenarios

### `test_integration.py`
Integration tests with real FastAPI apps:
- Debug mode behavior (detailed errors)
- Production mode behavior (secure errors)
- Security features (no sensitive headers)
- Consistent error format validation
- Comparison between debug and production modes

### `test_package.py`
Tests for package structure and imports:
- Public API availability
- Import paths and star imports
- Package metadata
- Exception inheritance chains

## Running Tests

### Prerequisites

Install test dependencies:

```bash
# Using uv (recommended)
uv sync --group test

# Or using pip
pip install pytest pytest-asyncio httpx
```

### Running All Tests

```bash
# Using uv (recommended)
uv run pytest tests/

# Or directly with pytest
pytest tests/

# With verbose output
uv run pytest tests/ -v
```

### Running Specific Test Files

```bash
# Test only exceptions
uv run pytest tests/test_exceptions.py -v

# Test only handlers
uv run pytest tests/test_handlers.py -v

# Test only integration
uv run pytest tests/test_integration.py -v
```

### Running Specific Test Classes or Methods

```bash
# Test specific class
uv run pytest tests/test_exceptions.py::TestSecurityHTTPException -v

# Test specific method
uv run pytest tests/test_handlers.py::TestSecureHttpExceptionHandler::test_404_exception -v
```

## Test Coverage

The test suite covers:

✅ **Exception Classes** (14 tests)
- Initialization with default and custom parameters
- Header handling
- Inheritance chain validation

✅ **Error Handlers** (13 tests)  
- All HTTP status codes (400, 401, 403, 404, 405, 422, 500, etc.)
- Validation error handling
- Starlette exception handling
- Security header removal

✅ **Setup Function** (9 tests)
- Debug mode detection (explicit and auto-detect)
- Production mode configuration
- Multiple setup scenarios
- Mode switching

✅ **Integration** (16 tests)
- Full FastAPI app testing
- Debug vs production behavior
- Security features validation
- Error format consistency

✅ **Package Structure** (8 tests)
- Import validation
- Public API testing
- Package metadata

**Total: 60 tests**

## Key Test Features

### Security Validation
- Ensures sensitive headers are not leaked
- Validates that production mode hides internal details
- Confirms consistent error message format

### Debug vs Production
- Tests that debug mode shows detailed errors for development
- Confirms production mode shows generic secure messages
- Validates auto-detection of debug settings

### Error Handler Coverage
- Tests all common HTTP status codes
- Validates FastAPI validation error handling
- Ensures Starlette compatibility

### Exception Testing
- Tests all custom exception classes
- Validates inheritance chains
- Confirms proper initialization

## Continuous Integration

The tests are designed to run in CI environments:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    uv sync --group test
    uv run pytest tests/ --tb=short
```

## Test Configuration

Tests are configured via `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = ["-ra", "--strict-markers", "--strict-config", "--showlocals", "-v"]
testpaths = ["tests"]
asyncio_mode = "auto"
```

## Writing New Tests

When adding new features, ensure you:

1. **Add unit tests** for individual components
2. **Add integration tests** for end-to-end functionality  
3. **Test both debug and production modes** where applicable
4. **Follow the existing test structure** and naming conventions
5. **Include docstrings** explaining what each test validates

Example test pattern:

```python
class TestNewFeature:
    """Test the new feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality works as expected."""
        # Arrange
        # Act  
        # Assert
        
    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async functionality."""
        # For async tests
```
