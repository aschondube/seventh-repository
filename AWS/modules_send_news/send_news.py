import psycopg2
import json
import os

def send_data(event, context):
    try:
        print("Event received:", event)
        
        # Extract news data from the event
        news_data = event.get('responsePayload', {}).get('body', [])
        print("News data extracted:", news_data)

        # Ensure news_data is a list
        if not isinstance(news_data, list):
            raise ValueError("news_data should be a list")

        # Retrieve database connection URL from environment variable
        db_url = os.getenv('db_url')
        print("Database URL:", db_url)

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        print("Database connection established")

        # Prepare SQL statement for insertion
        insert_query = """
            INSERT INTO btc_news (date, title)
            VALUES (%s, %s)
            ON CONFLICT (title) DO NOTHING
        """
        print("Insert query prepared")

        # Iterate through each item in the list
        for item in news_data:
            print("Processing item:", item)
            # Extract date and title from the item
            date = item.get('Date')
            title = item.get('Title')
            if date and title:
                # Execute the insert query
                cur.execute(insert_query, (date, title))
                print("Inserted:", date, title)

        # Commit the changes to the database
        conn.commit()
        print("Database commit successful")

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully sent data to PostgreSQL database')
        }
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps(error_message)
        }
    finally:
        # Ensure the cursor and connection are closed properly
        if 'cur' in locals():
            cur.close()
            print("Cursor closed")
        if 'conn' in locals():
            conn.close()
            print("Connection closed")
