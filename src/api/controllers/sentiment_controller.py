from fastapi import APIRouter, Query, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Optional
import pandas as pd
import io
import csv

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


@router.post("/analyze-csv", response_model=SentimentResponse, status_code=200)
async def analyze_csv(
    file: UploadFile = File(...),
    use_case: SentimentAnalyzerUseCase = Depends(get_sentiment_analyzer_use_case)
) -> SentimentResponse:
    """
    Analyze sentiment of comments from a CSV file.
    
    Args:
        file: CSV file containing comments (should have a 'comment' column).
        use_case: Sentiment analyzer use case (injected).
        
    Returns:
        A response containing sentiment analysis results.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Check if 'comment' or 'Comment' column exists
        comment_column = None
        if 'comment' in df.columns:
            comment_column = 'comment'
        elif 'Comment' in df.columns:
            comment_column = 'Comment'
        else:
            raise HTTPException(
                status_code=400, 
                detail="CSV must contain a 'comment' or 'Comment' column"
            )
        
        # Extract comments and filter out empty ones
        comments = df[comment_column].dropna().astype(str).tolist()
        
        if not comments:
            raise HTTPException(status_code=400, detail="No valid comments found in CSV")
        
        # Create request object and analyze
        request = CommentRequest(comments=comments)
        return use_case.analyze_comments(request, include_details=True)
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/download-csv")
async def download_csv(results: SentimentResponse):
    """
    Generate and download a CSV file with sentiment analysis results.
    
    Args:
        results: Sentiment analysis results to convert to CSV.
        
    Returns:
        StreamingResponse with CSV file.
    """
    try:
        # Create CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['comment', 'sentiment', 'compound_score', 'positive_score', 'negative_score', 'neutral_score', 'emojis'])
        
        # Write data rows
        for result in results.results:
            emojis_str = ','.join(result.emojis) if result.emojis else ''
            writer.writerow([
                result.comment,
                result.sentiment,
                result.scores.compound,
                result.scores.positive,
                result.scores.negative,
                result.scores.neutral,
                emojis_str
            ])
        
        # Add summary row
        writer.writerow([])  # Empty row
        writer.writerow(['SUMMARY'])
        writer.writerow(['Total Comments', results.summary.total_comments])
        writer.writerow(['Positive Comments', results.summary.positive_comments])
        writer.writerow(['Negative Comments', results.summary.negative_comments])
        writer.writerow(['Neutral Comments', results.summary.neutral_comments])
        writer.writerow(['Positive Percentage', f"{results.summary.positive_percentage:.1f}%"])
        writer.writerow(['Negative Percentage', f"{results.summary.negative_percentage:.1f}%"])
        writer.writerow(['Neutral Percentage', f"{results.summary.neutral_percentage:.1f}%"])
        writer.writerow(['Average Compound Score', results.summary.average_compound])
        
        # Create response
        output.seek(0)
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type='text/csv',
            headers={"Content-Disposition": "attachment; filename=sentiment_analysis_results.csv"}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate CSV: {str(e)}")