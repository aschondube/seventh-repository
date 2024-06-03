# file to retrieve data from railway hosted DB and to send it onto streamlit
import pandas as pd 
import streamlit as st
from psycopg2 import sql
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# below function establishes connection with cloud hosted db
def get_db_connection():
    db_url = os.getenv('db_url')
    # db_url = st.secrets('db_url')
    engine = create_engine(db_url)
    return engine

# function to retrieve data from db
def fetch_bitcoin_prices(engine):
    query = "SELECT * FROM btc_prices ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

# function to retrieve data from db
def fetch_bitcoin_news(engine):
    query = "SELECT * FROM btc_news ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

conn = get_db_connection() # establishing the connector to the db

# fetching the data from the sql db passing the function-queries created above 
btc_prices_df = fetch_bitcoin_prices(conn)
btc_news_df = fetch_bitcoin_news(conn)

# creating a simple line chart for prices
st.title('Prices for BTC in the past 6 months')
st.line_chart(btc_prices_df.set_index('date')['close'])

# displaying the dataframe with btc news 
st.title("FT's BTC news in the past 6 months")
st.write(btc_news_df)