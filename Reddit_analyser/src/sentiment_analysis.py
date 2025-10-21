from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        
        if scores['compound'] > 0.05:
            return "positive"
        elif scores['compound'] < -0.05:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "neutral"

def calculate_sentiment_distribution(results):
    sentiment_counts = {
        'positive': 0,
        'negative': 0,
        'neutral': 0
    }

    for result in results:
        sentiment_counts[result['sentiment']] += 1

    total = len(results)
    
    if total == 0:
        print("No results found to analyze")
        return {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }

    return {
        'positive': (sentiment_counts['positive'] / total) * 100,
        'negative': (sentiment_counts['negative'] / total) * 100,
        'neutral': (sentiment_counts['neutral'] / total) * 100
    } 