import streamlit as st
import pandas as pd
import plotly.express as px
from sentiment_engine import analyze_text, analyze_dataframe

st.set_page_config(page_title="Sentiment Analysis Dashboard", page_icon="💬", layout="wide")
st.title("💬 Sentiment Analysis")
st.caption("Analyze reviews, social media posts, and news text using NLP, sentiment lexicons, and emotion detection.")

with st.sidebar:
    st.header("Data")
    source = st.selectbox("Choose data source", ["Sample dataset", "Upload CSV"])
    st.markdown("CSV must contain a text column such as `text`, `review`, `content`, or `comment`.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"]) if source == "Upload CSV" else None

@st.cache_data
def load_sample():
    return pd.read_csv("data/sample_reviews.csv")

try:
    if source == "Sample dataset":
        df = load_sample()
    elif uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("Upload a CSV file to begin.")
        st.stop()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

text_candidates = [c for c in df.columns if c.lower() in ["text", "review", "content", "comment", "message", "post", "headline"]]
text_col = st.selectbox("Select the text column", df.columns.tolist(), index=df.columns.get_loc(text_candidates[0]) if text_candidates else 0)

if not pd.api.types.is_string_dtype(df[text_col]):
    df[text_col] = df[text_col].fillna("").astype(str)

results = analyze_dataframe(df, text_col)
st.subheader("Sentiment overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total texts", len(results))
c2.metric("Positive", int((results.sentiment == "Positive").sum()))
c3.metric("Negative", int((results.sentiment == "Negative").sum()))
c4.metric("Neutral", int((results.sentiment == "Neutral").sum()))

left, right = st.columns(2)
with left:
    counts = results["sentiment"].value_counts().rename_axis("Sentiment").reset_index(name="Count")
    st.plotly_chart(px.pie(counts, names="Sentiment", values="Count", hole=0.45, title="Sentiment distribution"), use_container_width=True)
with right:
    emotion_cols = ["joy", "sadness", "anger", "fear", "surprise", "trust"]
    emotion_totals = results[emotion_cols].sum().rename_axis("Emotion").reset_index(name="Matches")
    st.plotly_chart(px.bar(emotion_totals, x="Emotion", y="Matches", title="Emotion lexicon matches"), use_container_width=True)

if "source" in results.columns:
    st.subheader("Sentiment by source")
    by_source = results.groupby(["source", "sentiment"]).size().reset_index(name="Count")
    st.plotly_chart(px.bar(by_source, x="source", y="Count", color="sentiment", barmode="group"), use_container_width=True)

st.subheader("Analyzed records")
st.dataframe(results, use_container_width=True, hide_index=True)
csv = results.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download analyzed results", csv, "sentiment_results.csv", "text/csv")

st.subheader("Analyze one text")
single = st.text_area("Enter a review, post, or news sentence")
if st.button("Analyze text") and single.strip():
    result = analyze_text(single)
    st.write(f"**Sentiment:** {result['sentiment']}  |  **Compound score:** {result['compound']:.3f}")
    st.write("**Detected emotions:** " + (", ".join(result["emotions"]) if result["emotions"] else "No strong emotion keyword detected"))
    st.json(result)
