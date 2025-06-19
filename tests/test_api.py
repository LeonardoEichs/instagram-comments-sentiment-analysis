import pytest
from fastapi.testclient import TestClient
import sys
import os
import nltk
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Set NLTK data path to local directory
nltk_data_dir = os.path.join(project_root, "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.insert(0, nltk_data_dir)

# Download NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', download_dir=nltk_data_dir)

from src.api.app import app


class TestSentimentAPI:
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test that the root endpoint returns a successful response."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Instagram Comment Sentiment Analysis API is running" in response.json()["message"]
    
    def test_analyze_endpoint(self, client):
        """Test the sentiment analysis endpoint."""
        test_comments = [
            "This is amazing! I love it!",
            "This is terrible, I hate it."
        ]
        
        response = client.post(
            "/sentiment/analyze",
            json={"comments": test_comments}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "summary" in data
        assert "total_comments" in data["summary"]
        assert data["summary"]["total_comments"] == 2
        assert "positive_comments" in data["summary"]
        assert "negative_comments" in data["summary"]
        assert "neutral_comments" in data["summary"]
        assert "positive_percentage" in data["summary"]
        assert "negative_percentage" in data["summary"]
        assert "neutral_percentage" in data["summary"]
        assert "average_compound" in data["summary"]
        
        # Results should not be included by default
        assert "results" not in data or data["results"] is None
    
    def test_analyze_with_details(self, client):
        """Test the sentiment analysis endpoint with detailed results."""
        test_comments = [
            "This is amazing! I love it!",
            "This is terrible, I hate it."
        ]
        
        response = client.post(
            "/sentiment/analyze?include_details=true",
            json={"comments": test_comments}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "summary" in data
        assert "results" in data
        assert len(data["results"]) == 2
        
        # Check first result
        first_result = data["results"][0]
        assert "comment" in first_result
        assert "sentiment" in first_result
        assert "scores" in first_result
        assert "compound" in first_result["scores"]
        assert "positive" in first_result["scores"]
        assert "negative" in first_result["scores"]
        assert "neutral" in first_result["scores"]
        assert "emojis" in first_result
        
    def test_empty_comment_list(self, client):
        """Test the sentiment analysis endpoint with an empty comment list."""
        response = client.post(
            "/sentiment/analyze",
            json={"comments": []}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "summary" in data
        assert data["summary"]["total_comments"] == 0
        assert data["summary"]["positive_comments"] == 0
        assert data["summary"]["negative_comments"] == 0
        assert data["summary"]["neutral_comments"] == 0
        assert data["summary"]["positive_percentage"] == 0
        assert data["summary"]["negative_percentage"] == 0
        assert data["summary"]["neutral_percentage"] == 0
        assert data["summary"]["average_compound"] == 0