from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(tweet_texts):
    text = ' '.join(tweet_texts)  # Combine all tweet texts
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud for Hashtag Tweets')
    plt.savefig('static/hashtag_wordcloud.png')
    plt.close()
