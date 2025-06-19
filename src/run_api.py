import uvicorn
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def main():
    """Run the FastAPI server using Uvicorn."""
    # Get configuration from environment variables
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Determine if we're in production (disable reload in production)
    is_production = os.environ.get("ENVIRONMENT", "development") == "production"
    
    # Configure and run Uvicorn server
    uvicorn.run(
        "src.api.app:app",
        host=host,
        port=port,
        reload=not is_production,
        log_level="info"
    )


if __name__ == "__main__":
    main()