import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import emoji

from src.sentiment_analysis.emoji_utils import (
    get_emoji_sentiment_scores, 
    combine_sentiment_scores, 
    extract_emojis, 
    EMOJI_SENTIMENT
)

class SentimentAnalyzer:
    """Class for analyzing the sentiment of Instagram comments."""
    
    def __init__(self, model_type="vader", emoji_weight=0.3):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_type (str): The type of model to use for sentiment analysis.
                Currently only supports "vader" (rule-based).
            emoji_weight (float): Weight to give to emoji sentiment scores (0-1).
                Higher values give more importance to emojis.
        """
        self.model_type = model_type
        self.emoji_weight = emoji_weight
        
        if model_type == "vader":
            # Download required NLTK resources if not already downloaded
            try:
                nltk.data.find('vader_lexicon')
            except LookupError:
                nltk.download('vader_lexicon')
            
            self.analyzer = SentimentIntensityAnalyzer()
        
        else:
            raise ValueError("Invalid model_type. Currently only 'vader' is supported.")
    
    def analyze_comment(self, comment):
        """
        Analyze the sentiment of a single comment.
        
        Args:
            comment (str): The comment to analyze.
            
        Returns:
            dict: A dictionary containing sentiment scores and classification.
        """
        if not comment or not isinstance(comment, str):
            return {"compound": 0, "positive": 0, "negative": 0, "neutral": 0, "sentiment": "neutral", "emojis": []}
        
        # Extract emojis
        emojis = extract_emojis(comment)
        
        # Get VADER sentiment scores
        vader_scores = self.analyzer.polarity_scores(comment)
        
        # Get emoji sentiment scores
        emoji_scores = get_emoji_sentiment_scores(comment)
        
        # For emoji-only content, give more weight to emoji scores
        emojis = extract_emojis(comment)
        is_emoji_only = len(emojis) > 0 and len(comment.strip()) == len(''.join(emojis))
        
        # Use emoji scores directly for emoji-only content, or combine for mixed content
        if is_emoji_only and any(e in EMOJI_SENTIMENT for e in emojis):
            # For emoji-only content with known emojis, use emoji scores directly
            scores = emoji_scores
        else:
            # For mixed content or unknown emojis, combine scores
            scores = combine_sentiment_scores(vader_scores, emoji_scores, self.emoji_weight)
        
        # Determine sentiment based on compound score
        if scores['compound'] >= 0.05:
            sentiment = "positive"
        elif scores['compound'] <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "compound": scores["compound"],
            "positive": scores["pos"],
            "negative": scores["neg"],
            "neutral": scores["neu"],
            "sentiment": sentiment,
            "emojis": emojis
        }
    
    def analyze_comments(self, comments):
        """
        Analyze the sentiment of multiple comments.
        
        Args:
            comments (list): A list of comments to analyze.
            
        Returns:
            pd.DataFrame: A DataFrame containing the sentiment analysis results.
        """
        results = []
        
        for comment in comments:
            result = self.analyze_comment(comment)
            result["comment"] = comment
            results.append(result)
        
        return pd.DataFrame(results)
    
    def get_summary_stats(self, df):
        """
        Get summary statistics from a DataFrame of sentiment analysis results.
        
        Args:
            df (pd.DataFrame): DataFrame containing sentiment analysis results.
            
        Returns:
            dict: Dictionary containing summary statistics.
        """
        if df.empty:
            return {
                "total_comments": 0,
                "positive_percentage": 0,
                "negative_percentage": 0,
                "neutral_percentage": 0,
                "average_compound": 0
            }
        
        total = len(df)
        sentiment_counts = df["sentiment"].value_counts()
        
        positive = sentiment_counts.get("positive", 0)
        negative = sentiment_counts.get("negative", 0)
        neutral = sentiment_counts.get("neutral", 0)
        
        return {
            "total_comments": total,
            "positive_comments": positive,
            "negative_comments": negative,
            "neutral_comments": neutral,
            "positive_percentage": (positive / total) * 100 if total > 0 else 0,
            "negative_percentage": (negative / total) * 100 if total > 0 else 0,
            "neutral_percentage": (neutral / total) * 100 if total > 0 else 0,
            "average_compound": df["compound"].mean()
        }