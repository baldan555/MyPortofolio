from transformers import pipeline

# Menggunakan model pre-trained dari Hugging Face
classifier = pipeline('sentiment-analysis')

def analyze_sentiment(text):
    result = classifier(text)
    return result
