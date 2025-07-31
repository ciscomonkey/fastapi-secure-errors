from fastapi import FastAPI
from fastapi_secure_errors import setup_secure_error_handlers, SecureNotFound, SecureMethodNotAllowed
import os

# Create app with debug mode (can be set via environment or config)
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
print(f"Debug mode is set to: {debug_mode}")

app = FastAPI(debug=debug_mode)
#app = FastAPI(debug=True)  # Set to False for production

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