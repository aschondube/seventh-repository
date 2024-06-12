# import relevant modules

import pandas as pd 
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import plotly.express as px

load_dotenv()

st.set_page_config(layout="wide")

# Add custom CSS to adjust layout
st.markdown(
    """
    <style>
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    .css-1d391kg {
        padding-top: 1rem;
        padding-right: 5rem;
        padding-bottom: 1rem;
        padding-left: 5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Below function establishes connection with cloud hosted db
def get_db_connection():
    db_url1 = os.getenv('db_url1')
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

# Aggregate the merged_df to ensure unique dates by taking the mean of duplicate dates
merged_df_agg = merged_df.groupby('date').agg({
    'close': 'mean',
    'volume': 'mean',
    'title': lambda x: ' | '.join(x.dropna().unique())
}).reset_index()

# Convert the date column to datetime format in btc_news_df as well
btc_news_df['date'] = pd.to_datetime(btc_news_df['date'])

# Convert pandas Timestamps to datetime.date
min_date = merged_df_agg['date'].min().date()
max_date = merged_df_agg['date'].max().date()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Price-News Analysis", "News-NLP Analysis"])

# Function to display the Price-News Analysis Page
def price_news_analysis():
    st.title("Bitcoin Price Analysis with News Correlation")

    # Date range slider
    date_range = st.slider("**Select Date Range to adjust the line chart above ↑**", min_date, max_date, (min_date, max_date))

    # Filter the dataframe based on the selected date range
    filtered_df = merged_df_agg[(merged_df_agg['date'] >= pd.to_datetime(date_range[0])) & (merged_df_agg['date'] <= pd.to_datetime(date_range[1]))]

    # Creating a Plotly line chart with tooltips for news
    y_axis = st.selectbox("Select the value for y-axis:", ["close", "volume"])
    fig = px.line(filtered_df, x='date', y=y_axis, title=f'BTC {y_axis.capitalize()} over Time', labels={y_axis: f'BTC {y_axis.capitalize()}'})

    # Calculate the average price or volume
    avg_value = filtered_df[y_axis].mean()

    # Add average line
    fig.add_scatter(x=filtered_df['date'], y=[avg_value] * len(filtered_df), mode='lines', name='Average')

    # Add hover data for news headlines
    fig.update_traces(mode='lines+markers', hovertemplate='<b>Date</b>: %{x}<br><b>Value</b>: %{y}<br><b>News</b>: %{customdata[0]}')
    fig.update_traces(customdata=filtered_df[['title']].values)

    # Display the Plotly chart
    st.plotly_chart(fig)

    # Create the news table with the BTC price and price change indicator
    btc_news_df1 = btc_news_df[['date', 'title']]
    btc_news_df1['price'] = btc_news_df1['date'].map(merged_df_agg.set_index('date')['close'])
    btc_news_df1['price_change'] = btc_news_df1['date'].map(merged_df_agg.set_index('date')['close'].diff().apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change'))

    # Apply color to price based on increase or decrease
    def color_price(val):
        color = 'green' if val == 'Increase' else 'red' if val == 'Decrease' else 'black'
        return f'color: {color}'

    # Displaying the dataframe with btc news
    st.title("FT's BTC news in the past 6 months")
    styled_news_df = btc_news_df1.style.applymap(color_price, subset=['price_change'])
    st.write(styled_news_df)

# Function to display the News-NLP Analysis Page
def news_nlp_analysis():
    st.title("Bitcoin News Sentiment Analysis")

    # Determine the predominant sentiment for each news article
    btc_news_df['predominant_sentiment'] = btc_news_df[['positive', 'neutral', 'negative']].idxmax(axis=1)

    # Create a pie chart for sentiment distribution
    sentiment_counts = btc_news_df['predominant_sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    fig_pie = px.pie(sentiment_counts, names='sentiment', values='count', title='Distribution of News Sentiments')
    st.plotly_chart(fig_pie)

    # Create a bar chart for NLP scores
    fig_nlp = px.bar(btc_news_df.melt(id_vars=['date', 'title'], value_vars=['positive', 'neutral', 'negative']),
                     x='date', y='value', color='variable',
                     title='NLP Sentiment Scores Over Time',
                     labels={'value': 'Sentiment Score'},
                     hover_data={'title': True})

    # Display the Plotly chart
    st.plotly_chart(fig_nlp)

    # Highlight the highest score for each news
    def highlight_max(row):
        scores = row[['positive', 'neutral', 'negative']]
        colors = ['color: black'] * len(row)
        max_idx = scores.idxmax()
        if max_idx == 'positive':
            colors[row.index.get_loc('positive')] = 'color: green'
        elif max_idx == 'neutral':
            colors[row.index.get_loc('neutral')] = 'color: yellow'
        elif max_idx == 'negative':
            colors[row.index.get_loc('negative')] = 'color: red'
        return colors

    # Ensure the date column is in the correct format
    btc_news_df['date'] = pd.to_datetime(btc_news_df['date']).dt.date

    # Displaying the dataframe with highlighted scores
    st.title("FT's BTC news with NLP sentiment scores")
    styled_news_nlp_df = btc_news_df[['date', 'title', 'positive', 'neutral', 'negative']].style.apply(highlight_max, axis=1)
    st.write(styled_news_nlp_df)

# Render the selected page
if page == "Price-News Analysis":
    price_news_analysis()
elif page == "News-NLP Analysis":
    news_nlp_analysis()

