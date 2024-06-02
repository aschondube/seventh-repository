# web scraping news from FT on BTC for dates in which we have prices

# relevant modules
import pandas as pd
import requests
import bs4
from bs4 import *
import os
import lxml
from datetime import datetime
from dateutil.relativedelta import relativedelta

def scrape_ft_bitcoin_articles():
    # Base URL of the Financial Times Bitcoin page
    base_url = 'https://www.ft.com/bitcoin'
    
    # Initialize the page counter
    page_number = 1
    
    # Prepare lists to store the extracted data
    article_dates = []
    article_titles = []
    
    # Define the cutoff date (exactly 6 months ago from today)
    cutoff_date = datetime.now().date() - relativedelta(months=6)

    while True:
        # Construct the URL for the current page
        url = f'{base_url}?page={page_number}'
        
        # Make the HTTP request
        result = requests.get(url)
        
        # Parse the HTML using BeautifulSoup
        soup = bs4.BeautifulSoup(result.text, 'html.parser')
        
        # Extract dates and titles
        dates = soup.select('time.o-date')
        titles = soup.select('a.js-teaser-heading-link')
        
        # Extract date and title text
        for date, title in zip(dates, titles):
            # Parse the date to keep only the date component
            parsed_date = datetime.fromisoformat(date.get('datetime')).date()
            
            # Check if the article date is within the last 6 months
            if parsed_date < cutoff_date:
                df = pd.DataFrame({
                    'Date': article_dates,
                    'Title': article_titles
                })
                df['Date'] = pd.to_datetime(df['Date'])
                return df
            
            article_dates.append(parsed_date)
            article_titles.append(title.get_text(strip=True))
        
        # Check for the presence of the "next page" link
        next_page_link = soup.find('a', class_='o-buttons-icon--arrow-right')
        
        # If there is no link to the next page, break out of the loop
        if not next_page_link:
            break
        
        # Increment the page number for the next iteration
        page_number += 1
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Date': article_dates,
        'Title': article_titles
    })
    
    # Ensure the Date column is in datetime dtype
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

bitcoin_articles_df = scrape_ft_bitcoin_articles()
print(bitcoin_articles_df)
