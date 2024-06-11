import requests
import os
import psycopg2

API_URL = os.getenv('url')
token = os.getenv('token')
headers = {"Authorization": f"Bearer {token}"}

def lambda_handler(event, context):
    # Extract the news data from the event
    news_data = event.get('news_data', {}).get('body', [])
    
    # Initialize a list to store the results
    results = []
    
    # Iterate through the news data and perform sentiment analysis
    for item in news_data:
        title = item['Title']
        response = requests.post(API_URL, headers=headers, json={"inputs": title})
        sentiment_result = response.json()
        results.append({
            "Date": item["Date"],
            "Title": title,
            "Sentiment": sentiment_result
        })
    
    # Return the results
    return {
        "statusCode": 200,
        "body": results
    }

