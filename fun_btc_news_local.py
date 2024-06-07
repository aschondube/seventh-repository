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

def scrape_ft_bitcoin_articles(event, context):
    # Base URL of the Financial Times Bitcoin page
    base_url = 'https://www.ft.com/bitcoin'
    
    # Initialize the page counter
    page_number = 1
    
    # Prepare lists to store the extracted data
    article_dates = []
    article_titles = []
    
    # Define the cutoff date (exactly a day / months / etc ago from today) - Note I've defaulted to a day to avoid overloading the db
    cutoff_date = datetime.now().date() - relativedelta(days=1)

    try:
        while True:
            # Construct the URL for the current page
            url = f'{base_url}?page={page_number}'
            
            # Make the HTTP request
            result = requests.get(url)
            result.raise_for_status()  # Check for request errors
            
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(result.text, 'html.parser')
            
            # Extract dates and titles
            dates = soup.select('time.o-date')
            titles = soup.select('a.js-teaser-heading-link')
            
            # Extract date and title text
            for date, title in zip(dates, titles):
                # Parse the date to keep only the date component
                parsed_date = datetime.fromisoformat(date.get('datetime')).date()
                
                # Check if the article date is within the last day
                if parsed_date < cutoff_date:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            'articles': [{'Date': str(d), 'Title': t} for d, t in zip(article_dates, article_titles)]
                        })
                    }
                
                article_dates.append(parsed_date)
                article_titles.append(title.get_text(strip=True))
            
            # Check for the presence of the "next page" link
            next_page_link = soup.find('a', class_='o-buttons-icon--arrow-right')
            
            # If there is no link to the next page, break out of the loop
            if not next_page_link:
                break
            
            # Increment the page number for the next iteration
            page_number += 1

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
    # Create a list of dictionaries
    articles = [{'Date': str(date), 'Title': title} for date, title in zip(article_dates, article_titles)]
    
    # Return the JSON response
    return {
        'statusCode': 200,
        'body': json.dumps({'articles': articles})
    }


mock_event = {}
mock_context = None

response = scrape_ft_bitcoin_articles(mock_event, mock_context)
print(response)

# Uncomment the line below for local testing
# print(scrape_ft_bitcoin_articles({}, None))