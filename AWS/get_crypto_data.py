# call to alphavantage api to get data on a temporal basis (defaulted to daily) 
import requests
import json
import urllib3
import os

def get_crypto_data(event, context):
  """
  Retrieves crypto data from Alpha Vantage API and returns it as JSON.

  Args:
      event (dict): Event data containing "symbol", "market", and "past_months" keys.
      context (object): Lambda context object (not directly used in this function).

  Returns:
      dict: Response object with status code and JSON body.
  """

  # Extract parameters from event
  symbol = event.get('symbol', 'BTC')
  market = event.get('market', 'USD')
  past_months = event.get('past_months', 6)

  # Define API endpoint and parameters
  base_url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&'
  # Load API key from environment variables (assuming you have set it up)
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
  
  # Convert time series data to dictionary (prevents dataframe overhead)
  crypto_data = dict(time_series_data)
  
  # Filter data for the past specified months (optional logic can be added here)
  # ... (implementation details omitted for brevity)

  # Return data as JSON
  #return json.dumps(crypto_data)
  return time_series_data


# Example usage (assuming Lambda context)
# event = {
#   'symbol': 'ETH',
#   'market': 'USD',
#   'past_months': 12
# }
# response = get_crypto_data(event, context)
# return {
#   'statusCode': 200,
#   'body': response
# }