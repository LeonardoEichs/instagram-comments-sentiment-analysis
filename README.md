# Instagram Comment Sentiment Analysis

A Python project for analyzing the sentiment of Instagram comments using VADER and transformer models. The project provides both a REST API and command-line interface for sentiment analysis with emoji support and visualization capabilities.

## Features

- Sentiment analysis of Instagram comments using VADER or transformer models
- Emoji support for improved sentiment detection
- REST API for analyzing comments via HTTP requests
- Visualization tools for sentiment results
- Clean architecture with separation of concerns
- Comprehensive test suite

## Project Structure

```
instagram-comment-sentiment-analysis/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── app.py             # Main FastAPI app configuration
│   │   ├── controllers/        # API endpoint handlers
│   │   ├── models/            # Pydantic data models
│   │   └── use_cases/         # Business logic layer
│   ├── sentiment_analysis/    # Core sentiment analysis logic
│   │   ├── analyzer.py        # Main sentiment analyzer
│   │   ├── emoji_utils.py     # Emoji processing utilities
│   │   └── visualizer.py      # Data visualization tools
│   ├── main.py               # CLI demo script
│   └── run_api.py            # API server runner
├── tests/                    # Test suite
│   ├── test_analyzer.py      # Sentiment analyzer tests
│   ├── test_api.py          # API endpoint tests
│   └── test_emoji_support.py # Emoji functionality tests
├── requirements.txt          # Python dependencies
└── Dockerfile               # Container configuration
```

## Installation

### Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd instagram-comment-sentiment-analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download NLTK data:
   ```bash
   python download_nltk_data.py
   ```

5. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Docker Installation

1. Build the Docker image:
   ```bash
   docker build -t instagram-sentiment .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 instagram-sentiment
   ```

## Running the API Server

Start the FastAPI server with:

```bash
python src/run_api.py
```

The API will be available at http://localhost:8000 with interactive documentation at http://localhost:8000/docs

## API Usage

### Analyze Comments

Endpoint: `POST /sentiment/analyze`

Request body:
```json
{
  "comments": [
    "This picture is so beautiful! I love it! ❤️",
    "Wow, amazing content as always! 👏",
    "This is terrible content, I'm unfollowing.",
    "Not impressed with this post. Expected better."
  ]
}
```

Optional query parameters:
- `include_details=true` - Include detailed analysis for each comment

Response:
```json
{
  "summary": {
    "total_comments": 4,
    "positive_comments": 2,
    "negative_comments": 2,
    "neutral_comments": 0,
    "positive_percentage": 50.0,
    "negative_percentage": 50.0,
    "neutral_percentage": 0.0,
    "average_compound": 0.1234
  },
  "results": [
    {
      "comment": "This picture is so beautiful! I love it! ❤️",
      "sentiment": "positive",
      "scores": {
        "compound": 0.876,
        "positive": 0.8,
        "negative": 0.0,
        "neutral": 0.2
      },
      "emojis": ["❤️"]
    },
    ...
  ]
}
```

## Running the CLI Demo

To run the command-line demo:

```bash
python src/main.py
```

This will analyze sample comments and generate visualization files in the `output` directory.

## Running Tests

The project includes a comprehensive test suite to ensure code quality and functionality.

### Run All Tests

```bash
pytest
```
### Run Specific Test Files

```bash
# Test sentiment analyzer
pytest tests/test_analyzer.py

# Test API endpoints
pytest tests/test_api.py

# Test emoji support
pytest tests/test_emoji_support.py
```