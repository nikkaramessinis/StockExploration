import feedparser

# Use a pipeline as a high-level helper
from transformers import pipeline

ticker = "META"
keyword = "meta"


ticker_to_keyword = {
    "AAPL": "MSFT"
    - GOOG
    - QCOM
    - AMD
    - AVGO
    - NVDA
    # - TSLA
    # - NFLX
    - SMCI
    # - LLY
}
pipe = pipeline("text-classification", model="ProsusAI/finbert")
rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}"
feed = feedparser.parse(rss_url)
total_score = 0
num_articles = 0
for i, entry in enumerate(feed.entries):
    if keyword.lower() not in entry.summary.lower():
        continue

    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print(f"Summary: {(entry.summary)}")
    sentiment = pipe(entry.summary)[0]
    print(f"Sentiment {sentiment['label']}. Score :{sentiment['score']}")
    print("-" * 40)
    if sentiment["label"] == "positive":
        total_score += sentiment["score"]
        num_articles += 1
    elif sentiment["label"] == "negative":
        total_score -= sentiment["score"]
        num_articles += 1

final_score = total_score / num_articles
print(f"Overall sentiment {'Positive' if total_score > 0.15 else 'Negative'}")
