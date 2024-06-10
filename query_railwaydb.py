# code to perform queries on the cloud railway postgresql db (query in case is a row deletion on a date condition) 

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()


path = os.getenv('db_url1')


with psycopg2.connect(path) as conn:
    cur = conn.cursor()
    try:
        delete_query = sql.SQL("DELETE FROM btc_prices WHERE date = %s")
        cur.execute(delete_query, ('2025-06-05',))
        rows_deleted = cur.rowcount
        conn.commit()
        print("Deletion successful")
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as error:
        print(f"Error deleting data: {error}")
    if rows_deleted > 0:
        print(f"{rows_deleted} row(s) deleted successfully")
    else:
        print("No rows found for deletion")

conn.close()