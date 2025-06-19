import uvicorn
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def main():
    """Run the FastAPI server using Uvicorn."""
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Configure and run Uvicorn server
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()