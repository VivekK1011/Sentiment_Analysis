import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

# Lightweight emotion lexicon for a clear, editable classroom demonstration.
EMOTION_LEXICON = {
    "joy": {"happy", "great", "excellent", "love", "amazing", "delight", "wonderful", "pleased", "enjoy", "awesome"},
    "sadness": {"sad", "disappointed", "unhappy", "poor", "regret", "miss", "upset", "sorry", "depressed"},
    "anger": {"angry", "hate", "annoyed", "furious", "worst", "terrible", "awful", "frustrated", "rude"},
    "fear": {"afraid", "scared", "worry", "worried", "risk", "unsafe", " डर", "fear", "concerned"},
    "surprise": {"surprised", "unexpected", "wow", "shocked", "astonishing", "suddenly"},
    "trust": {"reliable", "trusted", "secure", "honest", "recommend", "dependable", "safe", "quality"}
}

def clean_text(text):
    text = str(text or "")
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+|#(\w+)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def analyze_text(text):
    cleaned = clean_text(text)
    scores = _analyzer.polarity_scores(cleaned)
    if scores["compound"] >= 0.05:
        sentiment = "Positive"
    elif scores["compound"] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    words = set(re.findall(r"[a-zA-Z']+", cleaned.lower()))
    emotion_counts = {emotion: len(words & terms) for emotion, terms in EMOTION_LEXICON.items()}
    emotions = [emotion for emotion, count in emotion_counts.items() if count > 0]
    return {
        "cleaned_text": cleaned,
        "sentiment": sentiment,
        "positive_score": scores["pos"],
        "negative_score": scores["neg"],
        "neutral_score": scores["neu"],
        "compound": scores["compound"],
        **emotion_counts,
        "emotions": emotions
    }

def analyze_dataframe(df, text_col):
    output = df.copy()
    analyzed = output[text_col].fillna("").astype(str).apply(analyze_text).apply(pd.Series)
    return pd.concat([output.reset_index(drop=True), analyzed.reset_index(drop=True)], axis=1)
