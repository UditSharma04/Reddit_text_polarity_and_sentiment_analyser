import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_sentiment_distribution(sentiment_distribution):
        labels = ['Positive', 'Negative', 'Neutral']
        sizes = [
            sentiment_distribution['positive'],
            sentiment_distribution['negative'],
            sentiment_distribution['neutral']
        ]
        colors = ['green', 'red', 'blue']
        explode = (0.1, 0, 0)

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.title('Sentiment Analysis of Reddit Comments')
        plt.show() 