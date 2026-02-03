import uvicorn
import os
from app import app

if __name__ == "__main__":
    port_env = os.getenv("PORT", "8000")
    try:
        port = int(port_env)
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as e:
        raise ValueError(f"Invalid PORT environment variable: {e}")

    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=port,
        reload=os.getenv("RELOAD", "true").lower() in ("true", "1", "t")
    )
