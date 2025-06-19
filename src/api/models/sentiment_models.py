from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from enum import Enum


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class CommentRequest(BaseModel):
    comments: List[str] = Field(..., description="List of comments to analyze")


class SentimentScores(BaseModel):
    compound: float = Field(..., description="Overall sentiment score from -1 (negative) to 1 (positive)")
    positive: float = Field(..., description="Positive sentiment score (0-1)")
    negative: float = Field(..., description="Negative sentiment score (0-1)")
    neutral: float = Field(..., description="Neutral sentiment score (0-1)")


class CommentAnalysis(BaseModel):
    comment: str = Field(..., description="The original comment text")
    sentiment: SentimentType = Field(..., description="The sentiment classification")
    scores: SentimentScores = Field(..., description="Detailed sentiment scores")
    emojis: List[str] = Field(default=[], description="Emojis found in the comment")


class SentimentSummary(BaseModel):
    total_comments: int = Field(..., description="Total number of comments analyzed")
    positive_comments: int = Field(..., description="Number of positive comments")
    negative_comments: int = Field(..., description="Number of negative comments")
    neutral_comments: int = Field(..., description="Number of neutral comments")
    positive_percentage: float = Field(..., description="Percentage of positive comments")
    negative_percentage: float = Field(..., description="Percentage of negative comments")
    neutral_percentage: float = Field(..., description="Percentage of neutral comments")
    average_compound: float = Field(..., description="Average compound sentiment score")


class SentimentResponse(BaseModel):
    summary: SentimentSummary = Field(..., description="Summary statistics of sentiment analysis")
    results: Optional[List[CommentAnalysis]] = Field(None, description="Individual comment analysis results")