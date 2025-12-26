import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for generating plots
import matplotlib.pyplot as plt
import seaborn as sns

def generate_user_charts(user_data):
    # Example `user_data` format: {'positive': 10, 'neutral': 5, 'negative': 8}
    sentiments = list(user_data.keys())
    counts = list(user_data.values())

    # Bar Chart for User Sentiment Analysis
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiments, y=counts, palette="Purples_d")
    plt.title("User Sentiment Analysis Activity", fontsize=14, weight="bold")
    plt.xlabel("Sentiments", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.savefig("static/charts/user_sentiment_analysis.png", bbox_inches="tight")
    plt.close()

    print("User charts generated successfully!")
