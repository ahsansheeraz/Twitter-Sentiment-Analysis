import matplotlib.pyplot as plt
import seaborn as sns

def generate_hashtag_visualizations(sentiment_data):
    # Count the number of tweets for each sentiment
    sentiment_counts = {
        'Negative': 0,
        'Neutral': 0,
        'Positive': 0
    }
    
    for tweet in sentiment_data:
        sentiment_counts[tweet['sentiment'].capitalize()] += 1
    
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    colors = ['red', 'orange', 'green']  # Red for negative, orange for neutral, green for positive
    
    # Generate Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title('Hashtag Sentiment Distribution')
    plt.savefig('static/hashtag_pie_chart.png')
    plt.close()

    # Generate Bar Chart
    plt.figure(figsize=(8, 6))
    sns.barplot(x=labels, y=sizes, palette=colors)
    plt.title('Hashtag Sentiment Distribution (Bar Chart)')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Tweets')
    plt.savefig('static/hashtag_bar_chart.png')
    plt.close()
