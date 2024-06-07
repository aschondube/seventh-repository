# Project 7 - API data reetrieval
# In this project, data will be fetched from specific sites with the objective of successfully connecting to an API and getting data.
# This document contains initial test API calls to Alpha Vantage

print('Hello world!')

# importing known relevant modules

import requests
import datetime as dt
import pandas as pd
import urllib3
import json 

# API 

# Base URL from IEX API for fetching $TSLA stock data

base_url = 'https://api.iex.cloud/v1/data/core/' # url provided in iex gui 

api_key = 'pk_54799237f22d49b29d1a9135a0a1c3b3' # key/token used to authenticate user 

info = 'quote' # quote is specified to retrieve stock prices, as they may be other type of products, commodities one could get

stock = 'btc' # choose the stock ticker/symbol you want to retrieve data from

# Construct the full API request URL
url = base_url + info + '/'+ stock + '?token=' + api_key 

# Make a GET request to the OpenWeatherMap API and parse the response as JSON
response = requests.get(url).json()

print(response)




