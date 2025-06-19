import pytest
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.sentiment_analysis.analyzer import SentimentAnalyzer
from src.sentiment_analysis.emoji_utils import extract_emojis, get_emoji_sentiment_scores, combine_sentiment_scores, EMOJI_SENTIMENT


class TestEmojiSupport:
    
    def setup_method(self):
        """Set up the test environment before each test method."""
        self.analyzer = SentimentAnalyzer(emoji_weight=0.3)
        self.analyzer_emoji_heavy = SentimentAnalyzer(emoji_weight=0.7)
        
        # Test samples
        self.emoji_only_positive = "❤️❤️❤️"
        self.emoji_only_negative = "👎👎👎"
        self.text_positive_emoji_positive = "I love this! ❤️"
        self.text_negative_emoji_negative = "I hate this product 👎"
        self.text_positive_emoji_negative = "Love it 👎"
        self.text_negative_emoji_positive = "I hate this product 😍"
        self.emoji_neutral = "This is a statement 🤔"
        self.text_only_positive = "This is amazing and fantastic!"
        self.text_only_negative = "This is terrible and awful!"
        
    def test_extract_emojis(self):
        """Test extracting emojis from text."""
        wave = extract_emojis("Hello 👋 World! 🌎")
        assert len(wave) == 2
        assert "👋" in wave
        assert "🌎" in wave
        
        assert extract_emojis("No emojis here") == []
        
        hearts = extract_emojis("❤️👍😊")
        assert len(hearts) == 3
        assert any(e == "❤" or e == "❤️" for e in hearts)
        assert "👍" in hearts
        assert "😊" in hearts
        
        assert extract_emojis("") == []
        assert extract_emojis(None) == []
        
    def test_emoji_only_positive(self):
        """Test analyzing emoji-only positive content."""
        regular_result = self.analyzer.analyze_comment(self.emoji_only_positive)
        heavy_result = self.analyzer_emoji_heavy.analyze_comment(self.emoji_only_positive)
        
        # With emojis only, both should pick up positive sentiment
        assert len(regular_result["emojis"]) == 3
        assert len(heavy_result["emojis"]) == 3
        assert all(e == "❤" or e == "❤️" for e in regular_result["emojis"])
        
        # Sentiment should be classified correctly
        assert regular_result["sentiment"] == "positive"
        assert heavy_result["sentiment"] == "positive"
        
        # For emoji-only content, emoji-heavy analyzer should have more positive score
        # due to the higher weight given to emoji sentiment
        assert heavy_result["positive"] > 0
        assert regular_result["positive"] > 0
        
    def test_emoji_only_negative(self):
        """Test analyzing emoji-only negative content."""
        regular_result = self.analyzer.analyze_comment(self.emoji_only_negative)
        heavy_result = self.analyzer_emoji_heavy.analyze_comment(self.emoji_only_negative)
        
        assert len(regular_result["emojis"]) == 3
        assert len(heavy_result["emojis"]) == 3
        assert all(e == "👎" for e in regular_result["emojis"])
        
        # Sentiment should be classified correctly
        assert regular_result["sentiment"] == "negative"
        assert heavy_result["sentiment"] == "negative"
        
        # For emoji-only content, both analyzers should give the same score
        # since we use emoji scores directly
        assert heavy_result["negative"] == regular_result["negative"]
        
    def test_text_positive_emoji_positive(self):
        """Test analyzing text with matching positive emoji."""
        result = self.analyzer.analyze_comment(self.text_positive_emoji_positive)
        
        assert len(result["emojis"]) == 1
        assert any(e == "❤" or e == "❤️" for e in result["emojis"])
        assert result["sentiment"] == "positive"
        assert result["compound"] > 0.5  # Should be strongly positive
        
    def test_text_negative_emoji_negative(self):
        """Test analyzing text with matching negative emoji."""
        result = self.analyzer.analyze_comment(self.text_negative_emoji_negative)
        
        assert "👎" in result["emojis"]
        assert result["sentiment"] == "negative"
        assert result["compound"] < -0.5  # Should be strongly negative
        
    def test_mixed_signals(self):
        """Test analyzing text with contradicting emoji signals."""
        # Positive text + negative emoji
        pos_neg_regular = self.analyzer.analyze_comment(self.text_positive_emoji_negative)
        pos_neg_heavy = self.analyzer_emoji_heavy.analyze_comment(self.text_positive_emoji_negative)
        
        # Regular analyzer should favor text, emoji-heavy should favor emojis
        assert pos_neg_regular["sentiment"] == "positive"
        assert pos_neg_heavy["sentiment"] == "negative"
        
        # Negative text + positive emoji
        neg_pos_regular = self.analyzer.analyze_comment(self.text_negative_emoji_positive)
        neg_pos_heavy = self.analyzer_emoji_heavy.analyze_comment(self.text_negative_emoji_positive)
        
        # Regular analyzer should favor text, emoji-heavy should favor emojis
        assert neg_pos_regular["sentiment"] == "negative"
        assert neg_pos_heavy["sentiment"] == "positive"
        
    def test_combine_sentiment_scores(self):
        """Test combining VADER and emoji sentiment scores."""
        vader_scores = {"compound": 0.5, "pos": 0.6, "neg": 0.1, "neu": 0.3}
        emoji_scores = {"compound": -0.7, "pos": 0.0, "neg": 0.7, "neu": 0.3}
        
        # With low emoji weight, VADER should dominate
        low_weight_combined = combine_sentiment_scores(vader_scores, emoji_scores, emoji_weight=0.3)
        assert low_weight_combined["compound"] > 0  # Still positive overall
        
        # With high emoji weight, emojis should dominate
        high_weight_combined = combine_sentiment_scores(vader_scores, emoji_scores, emoji_weight=0.7)
        assert high_weight_combined["compound"] < 0  # Becomes negative overall
        
        # With no emojis, should return VADER scores
        no_emoji_scores = {"pos": 0, "neg": 0, "neu": 1, "compound": 0}
        unchanged = combine_sentiment_scores(vader_scores, no_emoji_scores, emoji_weight=0.5)
        assert unchanged == vader_scores