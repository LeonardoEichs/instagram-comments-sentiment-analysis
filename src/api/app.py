from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nltk
import os
from pathlib import Path

from src.api.controllers.sentiment_controller import router as sentiment_router

# Initialize the app
app = FastAPI(
    title="Instagram Comment Sentiment Analysis API",
    description="API for analyzing the sentiment of Instagram comments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up NLTK data directory
project_root = Path(__file__).parent.parent.parent.parent
nltk_data_dir = os.path.join(project_root, "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.insert(0, nltk_data_dir)

# Download NLTK data at startup if needed
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', download_dir=nltk_data_dir)

# Include routers
app.include_router(sentiment_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint to check if the API is running."""
    return {
        "message": "Instagram Comment Sentiment Analysis API is running.",
        "docs": "/docs"
    }