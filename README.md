# Sentiment Analysis

## Features
- Classifies text as Positive, Negative, or Neutral using VADER sentiment analysis.
- Uses an editable keyword lexicon to detect joy, sadness, anger, fear, surprise, and trust.
- Includes example review, social-media, and news-style records.
- Supports uploading your own CSV file.
- Shows sentiment distribution, emotion counts, source comparisons, and downloadable results.

## 1. Open the project in VS Code
Extract the ZIP file. In VS Code, open the extracted `Sentiment_Analysis` folder.

## 2. Open the terminal in the project folder
Make sure the terminal path ends with `Task_4_Sentiment_Analysis`.

## 3. Install dependencies (Windows PowerShell)
```powershell
py -m pip install -r requirements.txt
```
If `py` is not available, use your Python executable:
```powershell
& "C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m pip install -r requirements.txt
```

## 4. Run the Streamlit dashboard
```powershell
python -m streamlit run app.py
```
Or, with your Python 3.14 executable:
```powershell
& "C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m streamlit run app.py
```
Open the local URL shown in the terminal, usually http://localhost:8501.

## 5. Run command-line analysis
```powershell
python analysis.py
```
The results are saved as `sentiment_results.csv`.

## Dataset format
Your CSV should have a text column, for example:
```csv
source,text
Amazon,"The product quality is excellent and delivery was quick."
Social Media,"I am disappointed with this update."
News,"The new service launched today."
```
The dashboard lets you select the text column after uploading.

## Methodology
1. Text cleaning: remove URLs, mentions, and extra whitespace.
2. Sentiment scoring: VADER returns positive, negative, neutral, and compound scores.
3. Classification: compound >= 0.05 is Positive; <= -0.05 is Negative; otherwise Neutral.
4. Emotion detection: count emotion-related keywords using the included editable lexicon.
5. Trend analysis: aggregate sentiment and emotion patterns by source.

## Important limitations
- The included dataset is a small demonstration dataset, not a representative survey or live feed.
- Emotion detection is keyword-based and does not understand context, sarcasm, or complex language.
- VADER is designed mainly for English social-media-style text.
- Do not claim that sample data represents current public opinion. For real conclusions, collect a larger, permitted, representative dataset and document its source and collection date.
- Respect website terms, privacy rules, and rate limits when collecting reviews or social-media content.
