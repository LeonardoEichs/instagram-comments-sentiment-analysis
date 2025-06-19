from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from src.api.models.sentiment_models import CommentRequest, SentimentResponse
from src.api.use_cases.sentiment_analyzer_use_case import SentimentAnalyzerUseCase

router = APIRouter(
    prefix="/sentiment",
    tags=["sentiment"],
    responses={404: {"description": "Not found"}},
)


def get_sentiment_analyzer_use_case() -> SentimentAnalyzerUseCase:
    """Dependency injection for SentimentAnalyzerUseCase."""
    return SentimentAnalyzerUseCase(model_type="vader", emoji_weight=0.3)


@router.post("/analyze", response_model=SentimentResponse, status_code=200)
async def analyze_sentiment(
    request: CommentRequest,
    include_details: bool = Query(False, description="Include detailed analysis for each comment"),
    use_case: SentimentAnalyzerUseCase = Depends(get_sentiment_analyzer_use_case)
) -> SentimentResponse:
    """
    Analyze the sentiment of a list of Instagram comments.
    
    Args:
        request: Request object containing a list of comments.
        include_details: Whether to include detailed results for each comment.
        use_case: Sentiment analyzer use case (injected).
        
    Returns:
        A response containing sentiment analysis results.
    """
    try:
        return use_case.analyze_comments(request, include_details)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )