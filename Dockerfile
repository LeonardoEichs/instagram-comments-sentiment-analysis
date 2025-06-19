FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Download NLTK data
RUN python download_nltk_data.py

# Install the package in development mode
RUN pip install -e .

# Expose port for the API
EXPOSE 8000

# Default command to run the API
CMD ["python", "src/run_api.py"]