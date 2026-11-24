from transformers import pipeline

# FinBERT is a classifier: sentence in → label out. It cannot write text.
finbert = pipeline("text-classification", model="ProsusAI/finbert")
headlines = [
    "Apple reports record-breaking revenue in Q4 despite market slowdown",
    "Tesla stock falls after earnings miss expectations",
]

for healine in headlines:
    result = finbert(healine)
    print(f"Headline: {healine}")
    print((f"Sentiment: " + result[0]['label'] + " with score: " + str(result[0]['score'])))
