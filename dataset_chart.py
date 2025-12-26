import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for generating plots
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_dataset_charts():
    # Load the dataset
    file_path = "train.csv"
    if not os.path.exists(file_path):
        print("Dataset not found!")
        return
    
    df = pd.read_csv(file_path)
    
    # Assuming dataset has a 'sentiment' column with values like 'positive', 'negative', 'neutral'
    sentiment_counts = df['sentiment'].value_counts()

    # Bar Chart for Sentiment Distribution
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="Blues_d")
    plt.title("Sentiment Distribution in Dataset", fontsize=14, weight="bold")
    plt.xlabel("Sentiments", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.savefig("static/charts/dataset_sentiment_distribution.png", bbox_inches="tight")
    plt.close()

    # Pie Chart for Sentiment Proportion
    plt.figure(figsize=(8, 6))
    sentiment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Blues_d"))
    plt.title("Sentiment Proportion in Dataset", fontsize=14, weight="bold")
    plt.ylabel("")
    plt.savefig("static/charts/dataset_sentiment_pie.png", bbox_inches="tight")
    plt.close()

    print("Dataset charts generated successfully!")
