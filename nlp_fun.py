from unittest import result
import requests
import os
from dotenv import load_dotenv, dotenv_values

# API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
# token = os.getenv('token_hf')
# headers = {"Authorization": f"Bearer {token}"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
	
# output = query({
# 	"inputs": "Market has a bull day with exchanges closing at the highest trading volumes ever recorded",
# })

# print(output)


# test = {
#   "statusCode": 200,
#   "body": [
#     {
#       "Date": "2024-05-30",
#       "Title": "European bitcoin ETPs suffer mounting outflows"
#     },
#     {
#       "Date": "2024-05-24",
#       "Title": "British-Chinese bitcoin money launderer jailed for over 6 years"
#     },
#     {
#       "Date": "2024-05-24",
#       "Title": "Cryptofinance: into the ether"
#     },
#     {
#       "Date": "2024-05-23",
#       "Title": "SEC paves way for ethereum ETFs in boost for crypto"
#     }
#   ]
# }


# Load environment variables from a .env file if needed
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
token = os.getenv('token_hf')
headers = {"Authorization": f"Bearer {token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Example news data received from an API
news_data = {
  "statusCode": 200,
  "body": [
    {
      "Date": "2024-05-30",
      "Title": "European bitcoin ETPs suffer mounting outflows"
    },
    {
      "Date": "2024-05-24",
      "Title": "British-Chinese bitcoin money launderer jailed for over 6 years"
    },
    {
      "Date": "2024-05-24",
      "Title": "Cryptofinance: into the ether"
    },
    {
      "Date": "2024-05-23",
      "Title": "SEC paves way for ethereum ETFs in boost for crypto"
    }
  ]
}

def analyze_titles(news_data):
    results = []
    for article in news_data["body"]:
        title = article["Title"]
        output = query({"inputs": title})
        results.append({
            "Date": article["Date"],
            "Title": title,
            "Sentiment": output
        })
    return results

# Analyze the titles and print the results
analyzed_news = analyze_titles(news_data)
for result in analyzed_news:
    print(result)


# Load environment variables
# load_dotenv()

# API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
# token = os.getenv('token_hf')
# headers = {"Authorization": f"Bearer {token}"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# def analyze_news_titles(news_data):
#     results = []
#     for item in news_data['body']:
#         title = item['Title']
#         result = query({"inputs": title})
#         results.append({
#             "Date": item["Date"],
#             "Title": title,
#             "Sentiment": result
#         })
#     return results

# # Example news data
# example = {
#   "statusCode": 200,
#   "body": [
#     {
#       "Date": "2024-05-30",
#       "Title": "European bitcoin ETPs suffer mounting outflows"
#     },
#     {
#       "Date": "2024-05-24",
#       "Title": "British-Chinese bitcoin money launderer jailed for over 6 years"
#     },
#     {
#       "Date": "2024-05-24",
#       "Title": "Cryptofinance: into the ether"
#     },
#     {
#       "Date": "2024-05-23",
#       "Title": "SEC paves way for ethereum ETFs in boost for crypto"
#     }
#   ]
# }

# # Analyze the news titles
# analysis_results = analyze_news_titles(example)

# print(analysis_results)

# # Print the results and store in list
# for result in analysis_results:
#     print(f"Date: {result['Date']}, Title: {result['Title']}, Sentiment: {result['Sentiment']}")

