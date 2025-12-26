import requests

def fetch_user_tweets(username, limit):
    url = "https: here add url .com/user/tweets"
    querystring = {"username": username, "limit": limit}
    
    headers = {
        "key": "add your key",  # Replace with your API key
        "host": " add host here "
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            return response.json().get('tweets', [])  # Extract the tweets list
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
