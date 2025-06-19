import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class SentimentVisualizer:
    """Class for visualizing sentiment analysis results."""
    
    def __init__(self, figsize=(10, 6), style="whitegrid"):
        """
        Initialize the visualizer.
        
        Args:
            figsize (tuple): Figure size for plots.
            style (str): Seaborn style for plots.
        """
        self.figsize = figsize
        self.style = style
        sns.set_style(style)
    
    def plot_sentiment_distribution(self, results_df, title="Sentiment Distribution", save_path=None):
        """
        Plot the distribution of sentiments (positive, negative, neutral).
        
        Args:
            results_df (pd.DataFrame): DataFrame containing sentiment analysis results.
            title (str): Title for the plot.
            save_path (str, optional): Path to save the plot. If None, plot is displayed.
            
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        plt.figure(figsize=self.figsize)
        
        sentiment_counts = results_df["sentiment"].value_counts()
        ax = sentiment_counts.plot(kind="bar", color=["green", "red", "gray"])
        
        plt.title(title)
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        
        # Add count labels on top of bars
        for i, count in enumerate(sentiment_counts):
            ax.text(i, count + 0.1, str(count), ha="center")
        
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
            return None
        
        return plt.gcf()
    
    def plot_sentiment_scores(self, results_df, title="Sentiment Scores Distribution", save_path=None):
        """
        Plot the distribution of sentiment scores.
        
        Args:
            results_df (pd.DataFrame): DataFrame containing sentiment analysis results.
            title (str): Title for the plot.
            save_path (str, optional): Path to save the plot. If None, plot is displayed.
            
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        plt.figure(figsize=self.figsize)
        
        ax = sns.histplot(results_df["compound"], bins=20, kde=True)
        
        plt.title(title)
        plt.xlabel("Compound Score")
        plt.ylabel("Frequency")
        
        # Add vertical lines for sentiment thresholds
        plt.axvline(-0.05, color="red", linestyle="--", alpha=0.7)
        plt.axvline(0.05, color="green", linestyle="--", alpha=0.7)
        
        plt.text(-0.25, ax.get_ylim()[1] * 0.9, "Negative", color="red")
        plt.text(0.15, ax.get_ylim()[1] * 0.9, "Positive", color="green")
        plt.text(-0.02, ax.get_ylim()[1] * 0.9, "Neutral", color="gray")
        
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
            return None
        
        return plt.gcf()
    
    def plot_sentiment_over_time(self, results_df, datetime_col, title="Sentiment Over Time", save_path=None):
        """
        Plot sentiment over time.
        
        Args:
            results_df (pd.DataFrame): DataFrame containing sentiment analysis results.
            datetime_col (str): Name of the column containing datetime information.
            title (str): Title for the plot.
            save_path (str, optional): Path to save the plot. If None, plot is displayed.
            
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        if datetime_col not in results_df.columns:
            raise ValueError(f"Column {datetime_col} not found in DataFrame")
        
        # Ensure datetime column is in datetime format
        df = results_df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
            df[datetime_col] = pd.to_datetime(df[datetime_col])
        
        # Group by day and calculate average compound score
        df["date"] = df[datetime_col].dt.date
        daily_sentiment = df.groupby("date")["compound"].mean().reset_index()
        
        plt.figure(figsize=self.figsize)
        
        sns.lineplot(data=daily_sentiment, x="date", y="compound", marker="o")
        
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Average Compound Score")
        plt.axhline(0, color="gray", linestyle="--", alpha=0.5)
        
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
            return None
        
        return plt.gcf()
    
    def plot_top_positive_negative(self, results_df, n=5, title="Top Positive and Negative Comments", save_path=None):
        """
        Plot the top N most positive and negative comments.
        
        Args:
            results_df (pd.DataFrame): DataFrame containing sentiment analysis results.
            n (int): Number of top comments to display.
            title (str): Title for the plot.
            save_path (str, optional): Path to save the plot. If None, plot is displayed.
            
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        # Get top positive and negative comments
        top_positive = results_df.nlargest(n, "compound")
        top_negative = results_df.nsmallest(n, "compound")
        
        # Create a new figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1] * 1.5))
        
        # Plot positive comments
        sns.barplot(data=top_positive, x="compound", y=top_positive.index, ax=ax1, color="green")
        ax1.set_title(f"Top {n} Positive Comments")
        ax1.set_xlabel("Compound Score")
        ax1.set_ylabel("Comment Index")
        
        # Plot negative comments
        sns.barplot(data=top_negative, x="compound", y=top_negative.index, ax=ax2, color="red")
        ax2.set_title(f"Top {n} Negative Comments")
        ax2.set_xlabel("Compound Score")
        ax2.set_ylabel("Comment Index")
        
        plt.tight_layout()
        plt.suptitle(title, y=1.05)
        
        if save_path:
            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
            return None
        
        return fig