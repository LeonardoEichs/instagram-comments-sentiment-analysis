#!/usr/bin/env python3
"""
Simple client to test the Instagram Comment Sentiment Analysis API.
First start the API server with: python src/run_api.py
Then run this script: python test_api_client.py
"""

import requests
import json
import sys
import time

def analyze_comments(comments, include_details=False):
    """
    Send comments to the API for sentiment analysis.
    
    Args:
        comments (list): List of comments to analyze.
        include_details (bool): Whether to include detailed results for each comment.
        
    Returns:
        dict: The API response.
    """
    url = "http://localhost:8000/sentiment/analyze"
    if include_details:
        url += "?include_details=true"
        
    payload = {"comments": comments}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        sys.exit(1)

def main():
    """Main function to test the API."""
    # Sample comments
    test_comments = [
        "This picture is so beautiful! I love it! ❤️",
        "Wow, amazing content as always! 👏",
        "This is terrible content, I'm unfollowing.",
        "Not impressed with this post. Expected better.",
        "Just okay, nothing special.",
        "You are the best! Keep it up! 🔥",
        "Horrible post, wasted my time.",
        "This is mediocre at best.",
        "So inspiring! Thank you for sharing! 😍",
        "Meh, seen better."
    ]
    
    # Analyze with summary only
    print("Testing API with summary only...")
    result = analyze_comments(test_comments)
    print("\nSentiment Analysis Summary:")
    print(json.dumps(result["summary"], indent=2))
    
    # Analyze with detailed results
    print("\nTesting API with detailed results...")
    detailed_result = analyze_comments(test_comments, include_details=True)
    print("\nSentiment Analysis Results (first 2 comments):")
    print(json.dumps(detailed_result["results"][:2], indent=2))

if __name__ == "__main__":
    main()