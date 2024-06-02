# testing of Selenium module
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set environment variable for ChromeDriver path
chromedriver_path = "C:\\Users\\EWF\\OneDrive\\Documentos\\CABerlin\\Project 8\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver_path

# Initialize Chrome driver
driver = webdriver.Chrome()

# Replace with the URL you want to scrape
url = "https://quotes.toscrape.com/"

# Open the URL
driver.get(url)

# Wait for the element to be clickable
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.text")))

# Click on the element
element.click()

# Now you can continue scraping or performing other actions

# Close the browser
driver.quit()


