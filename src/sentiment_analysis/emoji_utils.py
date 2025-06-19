import re
import emoji

# Dictionary of common emojis and their sentiment scores
# Format: emoji: (positive_score, negative_score, neutral_score)
EMOJI_SENTIMENT = {
    # Positive emojis
    '❤️': (0.8, 0, 0.2),
    '❤': (0.8, 0, 0.2),  # Alternative heart representation
    '😊': (0.8, 0, 0.2),
    '😍': (0.9, 0, 0.1),
    '😘': (0.9, 0, 0.1),
    '😁': (0.8, 0, 0.2),
    '😃': (0.8, 0, 0.2),
    '😄': (0.8, 0, 0.2),
    '😀': (0.7, 0, 0.3),
    '🥰': (0.9, 0, 0.1),
    '👍': (0.7, 0, 0.3),
    '💯': (0.8, 0, 0.2),
    '🔥': (0.7, 0, 0.3),
    '✅': (0.6, 0, 0.4),
    '💪': (0.7, 0, 0.3),
    '👏': (0.7, 0, 0.3),
    '🎉': (0.8, 0, 0.2),
    '💕': (0.9, 0, 0.1),
    '💖': (0.9, 0, 0.1),
    '💙': (0.8, 0, 0.2),
    '💚': (0.8, 0, 0.2),
    '💛': (0.8, 0, 0.2),
    '💜': (0.8, 0, 0.2),
    '🧡': (0.8, 0, 0.2),
    '😉': (0.6, 0, 0.4),
    '💓': (0.8, 0, 0.2),
    '💗': (0.8, 0, 0.2),
    '👌': (0.7, 0, 0.3),
    '🤗': (0.8, 0, 0.2),
    
    # Negative emojis
    '😢': (0, 0.7, 0.3),
    '😭': (0, 0.8, 0.2),
    '😞': (0, 0.7, 0.3),
    '😔': (0, 0.6, 0.4),
    '😟': (0, 0.6, 0.4),
    '😠': (0, 0.8, 0.2),
    '😡': (0, 0.9, 0.1),
    '😤': (0, 0.7, 0.3),
    '😒': (0, 0.6, 0.4),
    '👎': (0, 0.7, 0.3),
    '😑': (0, 0.5, 0.5),
    '😕': (0, 0.5, 0.5),
    '😩': (0, 0.7, 0.3),
    '😫': (0, 0.7, 0.3),
    '😖': (0, 0.7, 0.3),
    '😣': (0, 0.6, 0.4),
    '😱': (0, 0.8, 0.2),
    '😨': (0, 0.7, 0.3),
    '😰': (0, 0.7, 0.3),
    '😥': (0, 0.6, 0.4),
    '😓': (0, 0.6, 0.4),
    '💔': (0, 0.8, 0.2),
    '🙄': (0, 0.5, 0.5),
    '🤢': (0, 0.8, 0.2),
    '🤮': (0, 0.9, 0.1),
    
    # Neutral/ambiguous emojis
    '😐': (0.1, 0.1, 0.8),
    '😶': (0.1, 0.1, 0.8),
    '🤔': (0.2, 0.2, 0.6),
    '🙂': (0.4, 0, 0.6),
    '😌': (0.4, 0, 0.6),
    '😏': (0.3, 0.2, 0.5),
    '😬': (0.2, 0.3, 0.5),
    '🤷': (0.1, 0.1, 0.8),
    '🤷‍♀️': (0.1, 0.1, 0.8),
    '🤷‍♂️': (0.1, 0.1, 0.8),
    '😮': (0.3, 0.2, 0.5),
    '😯': (0.3, 0.2, 0.5),
    '🧐': (0.4, 0, 0.6),
}

def extract_emojis(text):
    """
    Extract all emojis from text.
    
    Args:
        text (str): The text to extract emojis from.
        
    Returns:
        list: A list of emojis found in the text.
    """
    if not text:
        return []
    
    return [c for c in text if c in emoji.EMOJI_DATA]

def get_emoji_sentiment_scores(text):
    """
    Calculate sentiment scores based on emojis in the text.
    
    Args:
        text (str): The text containing emojis.
        
    Returns:
        dict: A dictionary with positive, negative, and neutral scores.
    """
    if not text:
        return {"pos": 0, "neg": 0, "neu": 1.0, "compound": 0}
    
    emojis = extract_emojis(text)
    
    if not emojis:
        return {"pos": 0, "neg": 0, "neu": 1.0, "compound": 0}
    
    pos_score = 0
    neg_score = 0
    neu_score = 0
    count = 0
    
    for emoji_char in emojis:
        emoji_char_clean = emoji_char.strip()
        # Handle heart emojis that might be represented differently
        if emoji_char_clean == "❤" or emoji_char_clean == "❤️":
            emoji_char_clean = "❤️"  # Use the variant with variation selector
            
        if emoji_char_clean in EMOJI_SENTIMENT:
            pos, neg, neu = EMOJI_SENTIMENT[emoji_char_clean]
            pos_score += pos
            neg_score += neg
            neu_score += neu
            count += 1
    
    # If we didn't find any of our known emojis
    if count == 0:
        return {"pos": 0, "neg": 0, "neu": 1.0, "compound": 0}
    
    # Normalize scores
    pos_score = pos_score / count
    neg_score = neg_score / count
    neu_score = neu_score / count
    
    # Calculate compound score (similar to VADER)
    compound = pos_score - neg_score
    
    # Ensure compound score has the right threshold for emoji-only content
    # This makes sure emoji-only content can be classified as positive/negative
    if pos_score > 0.6 and compound > 0:
        compound = max(compound, 0.05)  # Ensure it's positive enough to be classified
    elif neg_score > 0.6 and compound < 0:
        compound = min(compound, -0.05)  # Ensure it's negative enough to be classified
    
    return {
        "pos": pos_score,
        "neg": neg_score,
        "neu": neu_score,
        "compound": compound
    }

def combine_sentiment_scores(vader_scores, emoji_scores, emoji_weight=0.3):
    """
    Combine VADER and emoji sentiment scores.
    
    Args:
        vader_scores (dict): Sentiment scores from VADER.
        emoji_scores (dict): Sentiment scores from emoji analysis.
        emoji_weight (float): Weight to give emoji scores (0-1).
        
    Returns:
        dict: Combined sentiment scores.
    """
    # If no emojis, just return VADER scores
    if emoji_scores["pos"] == 0 and emoji_scores["neg"] == 0:
        return vader_scores
    
    vader_weight = 1 - emoji_weight
    
    combined = {
        "pos": vader_scores["pos"] * vader_weight + emoji_scores["pos"] * emoji_weight,
        "neg": vader_scores["neg"] * vader_weight + emoji_scores["neg"] * emoji_weight,
        "neu": vader_scores["neu"] * vader_weight + emoji_scores["neu"] * emoji_weight,
    }
    
    # Calculate compound score
    combined["compound"] = vader_scores["compound"] * vader_weight + emoji_scores["compound"] * emoji_weight
    
    return combined