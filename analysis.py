import pandas as pd
from sentiment_engine import analyze_dataframe

df = pd.read_csv("data/sample_reviews.csv")
results = analyze_dataframe(df, "text")
print("\nSENTIMENT COUNTS")
print(results["sentiment"].value_counts())
print("\nAVERAGE VADER SCORES")
print(results[["positive_score", "negative_score", "neutral_score", "compound"]].mean().round(3))
print("\nEMOTION MATCH COUNTS")
print(results[["joy", "sadness", "anger", "fear", "surprise", "trust"]].sum())
results.to_csv("sentiment_results.csv", index=False)
print("\nSaved: sentiment_results.csv")
