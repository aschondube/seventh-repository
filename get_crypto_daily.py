from http.client import responses
from dotenv import load_dotenv
import requests
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_crypto_data(event, context):
    """
    Retrieves crypto data from Alpha Vantage API and returns it as JSON.

    Args:
        event (dict): Event data containing "symbol", "market", "past_days", and "past_months".
        context (object): Lambda context object (not directly used in this function).

    Returns:
        dict: Response object with status code and JSON body.
    """
    
    # Extract parameters from event
    symbol = event.get('symbol', 'BTC')
    market = event.get('market', 'USD')
    past_days = event.get('past_days', None)
    past_months = event.get('past_months', None)
    
    # Define API endpoint and parameters
    base_url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&'
    load_dotenv() # disable for cloud usage / enable for local usage
    api_key = os.getenv('alpha_APIkey')
    
    # Check if API key exists
    if api_key is None:
        raise ValueError("API key not found. Please add to the .env file.")
    
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
    
    # Convert time series data to dictionary
    crypto_data = dict(time_series_data)
    
    # Determine the cutoff date based on past_days or past_months
    cutoff_date = None
    if past_days is not None:
        cutoff_date = datetime.now().date() - relativedelta(days=past_days)
    elif past_months is not None:
        cutoff_date = datetime.now().date() - relativedelta(months=past_months)
    
    # Filter data based on the cutoff date
    if cutoff_date:
        crypto_data = {date: data for date, data in crypto_data.items() if datetime.strptime(date, '%Y-%m-%d').date() >= cutoff_date}
    
    # Return filtered data as JSON
    return crypto_data

# Example usage (assuming Lambda context)

# context = {}
# event = {
#   'symbol': 'ETH',
#   'market': 'USD',
#   'past_days': 0
# }
# response = get_crypto_data(event, context)

# print(response)
# # return {
# #   'statusCode': 200,
# #   'body': response
# # }
