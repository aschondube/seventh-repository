# code to perform queries on the cloud railway postgresql db (query in case is a row deletion on a date condition) 

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()


path = os.getenv('db_url1')


with psycopg2.connect(path) as conn: # uncomment to execute your query
    cur = conn.cursor()
    try:
        delete_query = sql.SQL("DELETE FROM btc_prices")
        cur.execute(delete_query)
        rows_deleted = cur.rowcount
        conn.commit()
        print("Query is successful")
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as error:
        print(f"Error deleting data: {error}")
    if rows_deleted > 0:
        print(f"{rows_deleted} row(s) deleted successfully")
    else:
        print("No rows found for deletion")

conn.close()