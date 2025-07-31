# fastapi-secure-errors

**Security-first HTTP error handling for FastAPI.**

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-secure-errors)](https://pypi.org/project/fastapi-secure-errors/)
[![PyPI](https://img.shields.io/pypi/v/fastapi-secure-errors)](https://pypi.org/project/fastapi-secure-errors/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

`fastapi-secure-errors` is a plug-and-play library for FastAPI that enforces security best practices in your API’s error responses. By default, FastAPI and Starlette can expose detailed error information—such as allowed HTTP methods, validation details, or internal exception traces—that can unintentionally leak information about your application’s structure or logic.

This library provides a unified, security-focused approach to HTTP error handling, ensuring your API only returns generic, minimal error messages and never exposes sensitive details. It's designed for teams and organizations that want to harden their FastAPI applications against information disclosure vulnerabilities, while maintaining a consistent and professional API experience.

---

## Features

* **Removes sensitive headers:** Automatically strips headers like `Allow` from 405 Method Not Allowed responses, preventing enumeration of allowed methods.
* **Generic, minimal error messages:** Provides simplified, non-descriptive error messages for common HTTP status codes (e.g., 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 422 Unprocessable Entity, 500 Internal Server Error).
* **Consistent error response format:** Ensures all handled errors return a predictable JSON structure, typically `{"detail": "Error message"}`.
* **Easy integration:** Secure your entire FastAPI application with a single function call.
* **Customizable:** While providing secure defaults, the underlying exception handlers can be extended or modified for specific needs.
* **Works seamlessly with FastAPI and Starlette.**

---

## Why use `fastapi-secure-errors`?

* **Reduce information leakage:** Prevent attackers from gaining insights into your backend architecture, endpoint existence, or allowed operations.
* **Meet compliance requirements:** Adhere to security best practices and compliance standards (e.g., OWASP Top 10, PCI DSS) that recommend generic error handling.
* **Professional API design:** Offer a clean, consistent, and secure error experience to your API consumers.
* **Save development time:** Avoid writing repetitive custom exception handlers for every potential error scenario across your application.

---

## Installation

Install from PyPI using pip:

```bash
pip install fastapi-secure-errors
```

Or using uv:

```bash
uv add fastapi-secure-errors
```

### Development Installation

For development or to get the latest changes, you can install directly from the repository:

```bash
pip install git+https://github.com/ciscomonkey/fastapi-secure-errors.git
```

Or clone the repository and install locally:

```bash
git clone https://github.com/ciscomonkey/fastapi-secure-errors.git
cd fastapi-secure-errors
pip install -e .
```

---

## Quick Start

To secure your FastAPI application, simply import `setup_secure_error_handlers` and call it with your `FastAPI` app instance:

```python
# examples/demo.py
from fastapi import FastAPI
from fastapi_secure_errors import setup_secure_error_handlers, SecureNotFound, SecureMethodNotAllowed
import os

# Create app with debug mode (can be set via environment or config)
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
app = FastAPI(debug=debug_mode)

# Setup secure error handlers
# Will automatically detect debug mode from app.debug
setup_secure_error_handlers(app)

# Or explicitly control debug mode:
# setup_secure_error_handlers(app, debug=False)  # Force secure mode
# setup_secure_error_handlers(app, debug=True)   # Force debug mode

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Use custom exceptions when needed
    if user_id < 1:
        raise SecureNotFound()
    
    return {"user_id": user_id}

@app.get("/protected")
async def protected_route():
    # This will automatically use secure error handling in production
    # but detailed error messages in debug mode
    return {"message": "Protected data"}
```

### Debug Mode vs Production Mode

By default, `fastapi-secure-errors` automatically detects whether your FastAPI app is running in debug mode:

- **Debug Mode (`app.debug=True`)**: Uses FastAPI's default error handlers, providing detailed error information for development
- **Production Mode (`app.debug=False`)**: Uses secure error handlers that provide minimal, generic error messages

This ensures you get helpful debugging information during development while maintaining security in production.

### Running the example:

1. For **development** (with detailed errors): `DEBUG=true fastapi dev examples/demo.py`
2. For **production** (with secure errors): `fastapi dev examples/demo.py` (DEBUG defaults to false)
3. Test with `http` or your browser:
    * `http GET :8000/users/0` -> In debug: detailed info, In production: `{"detail":"Resource not found"}`
    * `http POST :8000/users/1` (Method Not Allowed) -> In debug: detailed info, In production: `{"detail":"Method not allowed"}` (no `Allow` header)
    * `http GET :8000/nonexistent-path` -> In debug: FastAPI's default 404, In production: `{"detail":"Resource not found"}`

---

---

## Configuration

### Debug Mode Detection

The `setup_secure_error_handlers` function accepts an optional `debug` parameter:

```python
from fastapi import FastAPI
from fastapi_secure_errors import setup_secure_error_handlers

app = FastAPI()

# Auto-detect debug mode from app.debug (default behavior)
setup_secure_error_handlers(app)

# Explicitly set debug mode
setup_secure_error_handlers(app, debug=True)   # Force debug mode
setup_secure_error_handlers(app, debug=False)  # Force secure mode
```

**Auto-detection behavior:**
- If `debug=None` (default), the function checks `app.debug`
- If `app.debug=True`, uses FastAPI's default error handlers (detailed errors for development)
- If `app.debug=False`, uses secure error handlers (minimal errors for production)

**Common patterns:**
```python
import os

# Set debug based on environment variable
app = FastAPI(debug=os.getenv("DEBUG", "false").lower() == "true")
setup_secure_error_handlers(app)

# Or control directly via environment
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
setup_secure_error_handlers(app, debug=debug_mode)
```

### CLI Usage with `fastapi dev` and `fastapi run`

**Important Note**: The FastAPI CLI commands (`fastapi dev` and `fastapi run`) do **not** automatically set `app.debug=True/False`. They only control Uvicorn's behavior (like auto-reload). To use debug mode with CLI commands, you need to explicitly control the debug setting:

**Method 1: Using Environment Variables (Recommended)**
```python
import os
from fastapi import FastAPI
from fastapi_secure_errors import setup_secure_error_handlers

# Control debug mode via environment variable
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
app = FastAPI(debug=debug_mode)
setup_secure_error_handlers(app)
```

Then run with:
```bash
# Development with detailed errors
DEBUG=true fastapi dev app.py

# Production with secure errors  
fastapi dev app.py
# or explicitly: DEBUG=false fastapi dev app.py
```

**Method 2: Separate App Configurations**
```python
# dev_app.py
from fastapi import FastAPI
from fastapi_secure_errors import setup_secure_error_handlers

app = FastAPI(debug=True)  # Explicit debug mode
setup_secure_error_handlers(app)

# prod_app.py  
from fastapi import FastAPI
from fastapi_secure_errors import setup_secure_error_handlers

app = FastAPI(debug=False)  # Explicit production mode
setup_secure_error_handlers(app)
```

Then run with:
```bash
fastapi dev dev_app.py    # Uses debug mode
fastapi dev prod_app.py   # Uses production mode
```

---

## Custom Exceptions

The library also provides custom `SecurityHTTPException` classes for convenience, allowing you to raise specific secure errors directly:

```python
from fastapi_secure_errors import SecureMethodNotAllowed, SecureNotFound, SecureForbidden, SecureUnauthorized, SecureInternalServerError

# Example usage:
raise SecureNotFound(detail="The requested resource could not be found.")
raise SecureForbidden() # Uses default detail "Access denied"
```

These custom exceptions are automatically handled by `setup_secure_error_handlers` to ensure they conform to the secure response format.

---

## Development

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Ryan Mullins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```