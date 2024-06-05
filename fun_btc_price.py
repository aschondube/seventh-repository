# Retrieving BTC price from Alpha Vantage open API 

import requests
import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import json
import urllib3

def get_crypto_data(symbol='BTC', market='USD', past_months=6):
    # Define API endpoint and parameters
    base_url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&'
    load_dotenv('API.env')  # Load API key from environment variables
    api_key = os.getenv('alpha_APIkey')
    
    # Check if API key exists
    if api_key is None:
        raise ValueError("API key not found. Please set it in the API.env file.")
    
    # Construct the complete URL with API key, symbol, and market
    url = f"{base_url}symbol={symbol}&market={market}&apikey={api_key}"
    
    # Make a GET request to the API
    response = requests.get(url)
    
    # Check if request was successful (status code 200)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve data from API. Status code: {response.status_code}")
    
    # Extract JSON data from the response
    data = response.json()
    
    # Extract time series data from JSON
    time_series_data = data.get('Time Series (Digital Currency Daily)')
    
    if time_series_data is None:
        raise ValueError("Time series data not found in API response.")
    
    # Convert time series data to DataFrame
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    
    # Rename columns for readability
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    
    # Convert columns to float
    df = df.astype(float)
    
    # Convert index to datetime and sort
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    # Filter data for the past specified months
    if past_months is not None:
        cutoff_date = pd.Timestamp.today() - pd.DateOffset(months=past_months)
        df = df[df.index >= cutoff_date]
    
    # Reset the index to move the date from index to column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'date'}, inplace=True)
    
    return df

# Example usage:
crypto_df = get_crypto_data(past_months=6)  # Fetch data for the past 6 months
print(crypto_df)