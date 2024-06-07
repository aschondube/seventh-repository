# file to retrieve data from railway hosted DB and to send it onto streamlit
import pandas as pd 
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import plotly.express as px
from datetime import datetime

load_dotenv()

# Below function establishes connection with cloud hosted db
def get_db_connection():
    #db_url1 = os.getenv('db_url1') 
    db_url1 = st.secrets['db_url1']
    engine = create_engine(db_url1)
    return engine

# Function to retrieve data from db
def fetch_bitcoin_prices(engine):
    query = "SELECT * FROM btc_prices ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

# Function to retrieve data from db
def fetch_bitcoin_news(engine):
    query = "SELECT * FROM btc_news ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

conn = get_db_connection() # Establishing the connector to the db

# Fetching the data from the SQL db passing the function-queries created above 
btc_prices_df = fetch_bitcoin_prices(conn)
btc_news_df = fetch_bitcoin_news(conn)

# Merge prices and news dataframes on the date column
merged_df = pd.merge(btc_prices_df, btc_news_df, on='date', how='left')

# Convert the date column to datetime format
merged_df['date'] = pd.to_datetime(merged_df['date'])

# Convert pandas Timestamps to datetime.date
min_date = merged_df['date'].min().date()
max_date = merged_df['date'].max().date()

# Adding a date slider
date_range = st.slider("Select Date Range", min_date, max_date, (min_date, max_date))

# Filter the dataframe based on the selected date range
filtered_df = merged_df[(merged_df['date'] >= pd.to_datetime(date_range[0])) & (merged_df['date'] <= pd.to_datetime(date_range[1]))]

# Creating a Plotly line chart with tooltips for news
fig = px.line(filtered_df, x='date', y='close', title='Prices for BTC', labels={'close': 'BTC Price'})

# Add hover data for news headlines
fig.update_traces(mode='lines+markers', hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: %{y}<br><b>News</b>: %{customdata[0]}')
fig.update_traces(customdata=filtered_df[['title']].values)

# Display the Plotly chart
st.plotly_chart(fig)

# Displaying the dataframe with btc news
st.title("FT's BTC news in the past 6 months")
st.write(btc_news_df)
