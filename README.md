# Instagram Comment Sentiment Analysis

A Python project for analyzing the sentiment of Instagram comments using VADER and transformer models. The project provides both a web interface and REST API for sentiment analysis with emoji support and CSV processing capabilities.

## Features

- 🎯 Sentiment analysis using VADER and transformer models
- 😊 Emoji support for improved sentiment detection  
- 🌐 Web interface for CSV file upload and analysis
- 🔗 REST API for analyzing comments via HTTP requests
- 📊 CSV export with sentiment scores and summary statistics
- 🏗️ Clean architecture with separation of concerns
- 🧪 Comprehensive test suite
- 🐳 Docker support for easy deployment

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
│   │   └── emoji_utils.py     # Emoji processing utilities
│   ├── main.py               # CLI demo script
│   └── run_api.py            # API server runner
├── tests/                    # Test suite
│   ├── test_analyzer.py      # Sentiment analyzer tests
│   ├── test_api.py          # API endpoint tests
│   └── test_emoji_support.py # Emoji functionality tests
├── static/                   # Web interface files
│   └── index.html           # Frontend application
├── requirements.txt          # Python dependencies
├── sample_comments.csv       # Sample data for testing
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

## Usage

### Web Interface

1. Start the server: `python src/run_api.py`
2. Open your browser to `http://localhost:8000`
3. Upload a CSV file with a 'comment' or 'Comment' column
4. View analysis results and download the processed CSV

### API Server

The API will be available at http://localhost:8000 with interactive documentation at http://localhost:8000/docs

## API Endpoints

### 1. Analyze Comments (JSON)

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

### 2. Analyze CSV File

Endpoint: `POST /sentiment/analyze-csv`

Upload a CSV file with a 'comment' or 'Comment' column containing Instagram comments.

### 3. Download Results

Endpoint: `POST /sentiment/download-csv`

Download the sentiment analysis results as a CSV file with additional columns for sentiment scores and summary statistics.

## CSV File Format

Your CSV file should contain a column named either:
- `comment` (lowercase)
- `Comment` (uppercase)

Example CSV:
```csv
comment
"This is amazing! Love it! ❤️"
"Not impressed with this post"
"Great content as always! 👏"
```

The output CSV will include:
- Original comment text
- Sentiment classification (positive/negative/neutral)
- Detailed sentiment scores
- Detected emojis
- Summary statistics at the bottom

## CLI Demo

Run the command-line demo:

```bash
python src/main.py
```

This will analyze sample comments and display results in the terminal.

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

## Deployment

### Docker Deployment

The easiest way to deploy is using Docker:

```bash
# Build the image
docker build -t instagram-sentiment .

# Run in production
docker run -d -p 8000:8000 --name sentiment-app instagram-sentiment
```

### Environment Variables

For production deployment, you can configure:

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

### Health Check

Check if the API is running:
```bash
curl http://localhost:8000/docs
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Submit a pull request

## License

This project is open source and available under the MIT License.