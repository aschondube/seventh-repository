# function to use in pipeline to streamline data forwarding from the API call to the cloud database

import psycopg2
import json
import os

def send_data(event, context):
  """
  Sends retrieved crypto data to a PostgreSQL database using environment variables.

  Args:
      event (dict): Dictionary containing the event data (including crypto data in JSON format).
      context (object): Lambda context object (not used in this function).
  """

    # Check if 'crypto_data' key is in the event
    if 'crypto_data' not in event:
        print("Error: 'crypto_data' key not found in event")
        return


  # Extract crypto data from event
  crypto_data = event['crypto_data']

  # Retrieve database connection URL from environment variable
  db_url = os.getenv('db_url')

  # Connect to the PostgreSQL database
  try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
  except Exception as error:
    print(f"Error connecting to database: {error}")
    return

  # Prepare SQL statement for insertion (unchanged)
  insert_query = """
    INSERT INTO btc_prices(date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (date) DO NOTHING
  """

  # Iterate through each date-data pair in the JSON (unchanged)
  for date, daily_data in crypto_data.items():
    try:
      # Extract data from daily_data dictionary (unchanged)
      open_price = daily_data["1. open"]
      high_price = daily_data["2. high"]
      low_price = daily_data["3. low"]
      close_price = daily_data["4. close"]
      volume = daily_data["5. volume"]

      # Execute the insert query with specific data for each day (unchanged)
      cur.execute(insert_query, (date, open_price, high_price, low_price, close_price, volume))
    except Exception as error:
      print(f"Error inserting data for {date}: {error}")
      continue  # Continue to next date on error

  # Commit the changes to the database (unchanged)
  conn.commit()
  cur.close()
  conn.close()

  print("Successfully sent data to PostgreSQL database.")

# Example event to test the function locally
# event = {
#     'crypto_data': {
#         '2023-06-05': {
#             '1. open': 50000,
#             '2. high': 51000,
#             '3. low': 49000,
#             '4. close': 50500,
#             '5. volume': 1000
#         }
#     }
# }
# context = {}  # Lambda context object
# send_data(event, context)
