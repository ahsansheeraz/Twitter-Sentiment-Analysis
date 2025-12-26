import requests

def get_trends(country, limit):
    """Fetch the top trends for the given country and limit."""
    url = "https: here need to add link com/trends.php"
    headers = {
        "key": " here add key",
        "host": " here add host .com"
    }
    querystring = {"country": country}
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        trends_data = response.json()
        trend_list = trends_data.get("trends", [])
        return trend_list[:limit]  # Return the top 'limit' trends
    else:
        return None  # In case of failure, return None
