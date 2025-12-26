import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for generating plots
import matplotlib.pyplot as plt
import seaborn as sns

def generate_model_charts():
    # Example model metrics (Replace with actual model metrics)
    metrics = {
        "Accuracy": 0.89,
        "Precision": 0.87,
        "Recall": 0.85,
        "F1-Score": 0.86
    }
    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())

    # Bar Chart for Model Performance Metrics
    plt.figure(figsize=(8, 6))
    sns.barplot(x=metric_names, y=metric_values, palette="Greens_d")
    plt.title("Model Performance Metrics", fontsize=14, weight="bold")
    plt.ylim(0, 1)
    plt.xlabel("Metrics", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.savefig("static/charts/model_performance.png", bbox_inches="tight")
    plt.close()

    print("Model charts generated successfully!")
