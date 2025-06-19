import os
import sys
import pandas as pd
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.sentiment_analysis.analyzer import SentimentAnalyzer
from src.sentiment_analysis.visualizer import SentimentVisualizer

def main():
    """
    Sample script demonstrating the sentiment analysis functionality.
    """
    # Sample Instagram comments for demonstration
    sample_comments = [
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
    
    # Create output directories if they don't exist
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Initialize the sentiment analyzer (using VADER)
    print("Initializing sentiment analyzer...")
    analyzer = SentimentAnalyzer(model_type="vader")
    
    # Analyze comments
    print("Analyzing comments...")
    results = analyzer.analyze_comments(sample_comments)
    
    # Display results
    print("\nSentiment Analysis Results:")
    pd.set_option('display.max_colwidth', None)
    print(results[["comment", "sentiment", "compound"]].to_string(index=False))
    
    # Get summary statistics
    summary = analyzer.get_summary_stats(results)
    print("\nSummary Statistics:")
    for key, value in summary.items():
        if "percentage" in key:
            print(f"{key}: {value:.1f}%")
        else:
            print(f"{key}: {value}")
    
    # Visualize results
    print("\nGenerating visualizations...")
    visualizer = SentimentVisualizer()
    
    # Save the distribution plot
    fig1 = visualizer.plot_sentiment_distribution(results)
    fig1.savefig(output_dir / "sentiment_distribution.png", bbox_inches="tight", dpi=300)
    print(f"Saved sentiment distribution plot to: {output_dir / 'sentiment_distribution.png'}")
    
    # Save the scores plot
    fig2 = visualizer.plot_sentiment_scores(results)
    fig2.savefig(output_dir / "sentiment_scores.png", bbox_inches="tight", dpi=300)
    print(f"Saved sentiment scores plot to: {output_dir / 'sentiment_scores.png'}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()