import pg8000
import json
import os

def send_data(event, context):
    if 'crypto_data' not in event:
        print("Error: 'crypto_data' key not found in event")
        return

    crypto_data = event['crypto_data']
    db_url = os.getenv('db_url')

    try:
        conn = pg8000.connect(db_url)
        cur = conn.cursor()
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return

    insert_query = """
        INSERT INTO btc_prices(date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING
    """

    for date, daily_data in crypto_data.items():
        try:
            open_price = daily_data["1. open"]
            high_price = daily_data["2. high"]
            low_price = daily_data["3. low"]
            close_price = daily_data["4. close"]
            volume = daily_data["5. volume"]

            cur.execute(insert_query, (date, open_price, high_price, low_price, close_price, volume))
        except Exception as error:
            print(f"Error inserting data for {date}: {error}")
            continue

    conn.commit()
    cur.close()
    conn.close()

    print("Successfully sent data to PostgreSQL database.")
