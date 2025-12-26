import matplotlib.pyplot as plt
import io
import base64

def create_line_graph(trend_names, trend_count):
    """Generate line graph image."""
    # Sort data by trend count in descending order
    trend_names, trend_count = zip(*sorted(zip(trend_names, trend_count), key=lambda x: x[1], reverse=True))

    fig, ax = plt.subplots()
    ax.plot(trend_names, trend_count, marker='o')
    ax.set_title('Trend Name vs Tweets Volume (Line Graph)')
    ax.set_xlabel('Trend Name')
    ax.set_ylabel('Tweets Volume')

    # Save plot to a BytesIO buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_base64

def create_bar_graph(trend_names, trend_count):
    """Generate horizontal bar graph image."""
    # Sort data by trend count in descending order
    trend_names, trend_count = zip(*sorted(zip(trend_names, trend_count), key=lambda x: x[1], reverse=True))

    fig, ax = plt.subplots()
    ax.barh(trend_names, trend_count)  # Use horizontal bars instead of vertical
    ax.set_title('Trend Name vs Tweets Volume (Bar Graph)')
    ax.set_xlabel('Tweets Volume')
    ax.set_ylabel('Trend Name')

    # Save plot to a BytesIO buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_base64
