import pytest
import pandas as pd
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.sentiment_analysis.analyzer import SentimentAnalyzer

class TestSentimentAnalyzer:
    
    def setup_method(self):
        """Set up the test environment before each test method."""
        self.analyzer = SentimentAnalyzer(model_type="vader")
        
        self.positive_comment = "This is amazing! I love it!"
        self.negative_comment = "This is terrible, I hate it."
        self.neutral_comment = "This is a statement without emotion."
        
    def test_analyze_comment_positive(self):
        """Test analyzing a positive comment."""
        result = self.analyzer.analyze_comment(self.positive_comment)
        
        assert result["sentiment"] == "positive"
        assert result["compound"] > 0
        assert result["positive"] > result["negative"]
        
    def test_analyze_comment_negative(self):
        """Test analyzing a negative comment."""
        result = self.analyzer.analyze_comment(self.negative_comment)
        
        assert result["sentiment"] == "negative"
        assert result["compound"] < 0
        assert result["negative"] > result["positive"]
        
    def test_analyze_comment_neutral(self):
        """Test analyzing a neutral comment."""
        result = self.analyzer.analyze_comment(self.neutral_comment)
        
        assert result["sentiment"] == "neutral"
        assert -0.05 <= result["compound"] <= 0.05
        
    def test_analyze_comments(self):
        """Test analyzing multiple comments."""
        comments = [self.positive_comment, self.negative_comment, self.neutral_comment]
        
        results = self.analyzer.analyze_comments(comments)
        
        assert isinstance(results, pd.DataFrame)
        assert len(results) == 3
        assert "sentiment" in results.columns
        assert "compound" in results.columns
        assert "comment" in results.columns
        
    def test_get_summary_stats(self):
        """Test getting summary statistics."""
        # Explicitly create comments to ensure fixed sentiment results
        comments = [
            "This is amazing! I love it!",  # Positive
            "I am feeling very happy today.",  # Positive
            "This is terrible, I hate it.",  # Negative
            "This is a statement without emotion."  # Neutral
        ]
        results = self.analyzer.analyze_comments(comments)
        
        summary = self.analyzer.get_summary_stats(results)
        
        assert summary["total_comments"] == 4
        assert summary["positive_comments"] == 2
        assert summary["negative_comments"] == 1
        assert summary["neutral_comments"] == 1
        assert summary["positive_percentage"] == pytest.approx(50.0, 0.1)
        assert summary["negative_percentage"] == pytest.approx(25.0, 0.1)
        assert summary["neutral_percentage"] == pytest.approx(25.0, 0.1)
        
    def test_empty_comment(self):
        """Test handling empty comments."""
        result = self.analyzer.analyze_comment("")
        
        assert result["sentiment"] == "neutral"
        assert result["compound"] == 0
        
    def test_non_string_comment(self):
        """Test handling non-string comments."""
        result = self.analyzer.analyze_comment(None)
        
        assert result["sentiment"] == "neutral"
        assert result["compound"] == 0