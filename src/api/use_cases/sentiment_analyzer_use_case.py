from typing import List, Dict, Any, Optional
import pandas as pd
from src.sentiment_analysis.analyzer import SentimentAnalyzer
from src.api.models.sentiment_models import (
    CommentRequest,
    SentimentResponse,
    SentimentSummary,
    CommentAnalysis,
    SentimentScores,
    SentimentType
)


class SentimentAnalyzerUseCase:
    """Use case for analyzing sentiment of comments."""
    
    def __init__(self, model_type: str = "vader", emoji_weight: float = 0.3):
        """
        Initialize the sentiment analyzer use case.
        
        Args:
            model_type: The type of sentiment analysis model to use.
            emoji_weight: Weight to give to emoji sentiment (0-1).
        """
        self.analyzer = SentimentAnalyzer(model_type=model_type, emoji_weight=emoji_weight)
    
    def analyze_comments(self, request: CommentRequest, include_details: bool = False) -> SentimentResponse:
        """
        Analyze the sentiment of a list of comments.
        
        Args:
            request: The comment request containing the list of comments to analyze.
            include_details: Whether to include detailed results for each comment.
            
        Returns:
            A sentiment response containing summary statistics and optionally detailed results.
        """
        # Handle empty comment list
        if not request.comments:
            empty_summary = {
                "total_comments": 0,
                "positive_comments": 0,
                "negative_comments": 0,
                "neutral_comments": 0,
                "positive_percentage": 0,
                "negative_percentage": 0,
                "neutral_percentage": 0,
                "average_compound": 0
            }
            return SentimentResponse(summary=SentimentSummary(**empty_summary))
            
        # Analyze the comments using the analyzer
        df_results = self.analyzer.analyze_comments(request.comments)
        
        # Get summary statistics
        summary_stats = self.analyzer.get_summary_stats(df_results)
        summary = SentimentSummary(**summary_stats)
        
        # Create response
        response = SentimentResponse(summary=summary)
        
        # Include detailed results if requested
        if include_details:
            response.results = self._convert_to_comment_analysis_list(df_results)
        
        return response
    
    def _convert_to_comment_analysis_list(self, df: pd.DataFrame) -> List[CommentAnalysis]:
        """
        Convert analyzer results dataframe to a list of CommentAnalysis objects.
        
        Args:
            df: DataFrame containing sentiment analysis results.
            
        Returns:
            List of CommentAnalysis objects.
        """
        results = []
        
        for _, row in df.iterrows():
            scores = SentimentScores(
                compound=row["compound"],
                positive=row["positive"],
                negative=row["negative"],
                neutral=row["neutral"]
            )
            
            comment_analysis = CommentAnalysis(
                comment=row["comment"],
                sentiment=SentimentType(row["sentiment"]),
                scores=scores,
                emojis=row["emojis"]
            )
            
            results.append(comment_analysis)
            
        return results