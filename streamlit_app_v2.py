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
    db_url1 = os.getenv('db_url1')
    # db_url1 = st.secrets['db_url1']
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

conn = get_db_connection()  # Establishing the connector to the db

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

# App title
st.title("Bitcoin Price Analysis with News Correlation")

# Creating a Plotly line chart with tooltips for news
fig = px.line(merged_df, x='date', y='close', title='Prices for BTC', labels={'close': 'BTC Price'})

# Filter the dataframe based on the selected date range
filtered_df = merged_df[(merged_df['date'] >= pd.to_datetime(min_date)) & (merged_df['date'] <= pd.to_datetime(max_date))]

# Ensure unique dates by averaging prices for duplicate dates
filtered_df = filtered_df.groupby('date').agg({'close': 'mean', 'title': 'first'}).reset_index()

# Calculate the average price
avg_price = filtered_df['close'].mean()

# Add average price line
fig.add_scatter(x=filtered_df['date'], y=[avg_price] * len(filtered_df), mode='lines', name='Average Price')

# Calculate price change
filtered_df['price_change'] = filtered_df['close'].diff().fillna(0)
filtered_df['price_change'] = filtered_df['price_change'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')

# Add hover data for news headlines and price change
fig.update_traces(mode='lines+markers', hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: %{y}<br><b>News</b>: %{customdata[0]}<br><b>Change</b>: %{customdata[1]}')
fig.update_traces(customdata=filtered_df[['title', 'price_change']].values)

# Display the Plotly chart
st.plotly_chart(fig)

# Adding a date slider below the chart
date_range = st.slider("Select Date Range", min_date, max_date, (min_date, max_date))

# Filter the dataframe based on the selected date range
filtered_df = merged_df[(merged_df['date'] >= pd.to_datetime(date_range[0])) & (merged_df['date'] <= pd.to_datetime(date_range[1]))]

# Recalculate price change after filtering
filtered_df = filtered_df.groupby('date').agg({'close': 'mean', 'title': 'first'}).reset_index()
filtered_df['price_change'] = filtered_df['close'].diff().fillna(0)
filtered_df['price_change'] = filtered_df['price_change'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')

# Create the news table with the BTC price and price change indicator
btc_news_df['price'] = btc_news_df['date'].map(filtered_df.set_index('date')['close'])
btc_news_df['price_change'] = btc_news_df['date'].map(filtered_df.set_index('date')['price_change'])

# Apply color to price based on increase or decrease
def color_price(val):
    color = 'green' if val == 'Increase' else 'red' if val == 'Decrease' else 'black'
    return f'color: {color}'

# Displaying the dataframe with btc news
st.title("FT's BTC news in the past 6 months")
styled_news_df = btc_news_df.style.map(color_price, subset=['price_change'])
st.write(styled_news_df)



