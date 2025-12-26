from flask import Flask, render_template, request, jsonify,redirect, url_for, session,flash
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import re
import time 
import requests
from user_tweets import fetch_user_tweets
from auth import auth  # Import the Blueprint from auth.py
import os  # Make sure to import the os modules
#trends
from get_trends import get_trends
from trends_graphs import create_line_graph, create_bar_graph  # Importing graph functions
# Import visualization function
from hashtag_visualization import generate_hashtag_visualizations
from wordcloud_visualization import generate_wordcloud
#dashboard
from dataset_chart import generate_dataset_charts
from model_chart import generate_model_charts
from user_chart import generate_user_charts

app = Flask(__name__)


# Load the pre-trained model and vectorizer
model = load_model('sentiment_model.h5')
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Define stopwords
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 
             'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 
             'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
             'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
             'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
             'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
             'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 
             'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 
             'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 
             'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', 
             "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 
             'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', 
             "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def decontracted(phrase):
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def preprocess_text(text):
    text = decontracted(text)
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    text = ' '.join(e for e in text.split() if e.lower() not in stopwords)
    return text.lower().strip()

# Generate charts
generate_dataset_charts()
generate_model_charts()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    text = request.form['text']
    start_time = time.time()

    processed_input = preprocess_text(text)
    input_vectorized = vectorizer.transform([processed_input])
    prediction = model.predict(input_vectorized)
    
    sentiment = np.argmax(prediction)
    sentiment_label = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}[sentiment]

    total_time = time.time() - start_time
    print(f"Total Time: {total_time:.4f} seconds")

    return jsonify({'sentiment': sentiment_label})

@app.route('/hashtag_analysis', methods=['POST'])
def hashtag_analysis():
    hashtag = request.form['hashtag']
    count = int(request.form.get('count', 5))  # Default to 5 if not provided

    url = " #link to api data source"
    querystring = {"hashtag": hashtag, "limit": count, "section": "top"}
    
    headers = {
        "key": "here add key",
        "host": "here add host link.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        tweets = response.json().get('results', [])
        results = []
        tweet_texts = []

        for tweet in tweets:
            tweet_texts.append(tweet['text'])
            processed_input = preprocess_text(tweet['text'])
            input_vectorized = vectorizer.transform([processed_input])
            prediction = model.predict(input_vectorized)
            sentiment = np.argmax(prediction)
            sentiment_label = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}[sentiment]
            
            results.append({'text': tweet['text'], 'sentiment': sentiment_label})
        
        # Generate visualizations
        generate_hashtag_visualizations(results)
        generate_wordcloud(tweet_texts)

        return jsonify(results)
    else:
        return jsonify({'error': 'Failed to fetch data from RapidAPI'})

 
@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/analyze_trends', methods=['POST'])
def analyze_trends():
    try:
        # Parse JSON data
        data = request.get_json()
        country = data.get('country')
        trends_count = data.get('limit')

        # Debugging input values
        print("Country received:", country)
        print("Trends count received:", trends_count)

        # Validate input
        if not trends_count or not country:
            return jsonify({"error": "Country or trends count missing"}), 400

        trends_count = int(trends_count)  # Convert to integer
        
        # Fetch trends
        try:
            trends = get_trends(country, trends_count)[:trends_count]
            print("Fetched trends:", trends)  # Debugging fetched trends
        except Exception as e:
            print("Error in get_trends:", e)
            return jsonify({"error": "Error fetching trends"}), 500

        if not trends:
            print("Trends not found or empty")
            return jsonify({"error": "No trends found"}), 404

        # Prepare data for graphs
        trend_names = [trend.get("name", "No Name") for trend in trends]
        trend_count = [len(trend.get("name", "")) for trend in trends]

        # Generate graphs
        line_img = create_line_graph(trend_names, trend_count)
        bar_img = create_bar_graph(trend_names, trend_count)

        # Return results as JSON with image data in base64 format
        return jsonify({
            "trends": trends,
            "line_img": line_img,
            "bar_img": bar_img
        })

    except ValueError as ve:
        print("ValueError:", ve)
        return jsonify({"error": "Trends count must be an integer"}), 400

    except Exception as e:
        print("Exception:", e)
        return jsonify({"error": "Error fetching trends"}), 500

 # Set a secret key for sessions
app.secret_key = os.urandom(24)

# Register the auth Blueprint
app.register_blueprint(auth, url_prefix='/auth')

# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('auth.login'))
      # Fetch user data (example; replace with actual logic)
    user_data = {
        "positive": 10,
        "neutral": 5,
        "negative": 8
    }
    generate_user_charts(user_data)  # Generate charts for the logged-in user
    return render_template('dashboard.html', username=session.get('username'))

# Generate charts
generate_dataset_charts()
generate_model_charts()


if __name__ == '__main__':
    app.run(debug=True)
