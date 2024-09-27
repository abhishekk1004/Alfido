import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Optional: Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Use WebDriver Manager to handle driver installation automatically
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def fetch_page(url):
    try:
        driver = setup_driver()
        driver.get(url)
        return driver.page_source
    except Exception as e:
        print(f'Error setting up driver: {e}')
    finally:
        driver.quit()

def scrape_data(url, data_type, save_format):
    print(f'Scraping {data_type} from {url}...')
    html_content = fetch_page(url)
    if not html_content:
        print('Failed to fetch page. No data found.')
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    data = []

    if data_type == 'headlines':
        
        for item in soup.find_all('h2'):
            data.append(item.get_text(strip=True))

    elif data_type == 'images':
        for img in soup.find_all('img'):
            data.append(img['src'])

    elif data_type == 'audio':
        for audio in soup.find_all('audio'):
            data.append(audio['src'])

    

    if save_format == 'csv':
        pd.DataFrame(data).to_csv('scraped_data.csv', index=False)
        print('Data saved to scraped_data.csv')
    elif save_format == 'database':
        conn = sqlite3.connect('scraped_data.db')
        pd.DataFrame(data).to_sql('scraped_data', conn, if_exists='replace', index=False)
        print('Data saved to scraped_data.db')

def main():
    url = input('Enter the URL of the website you want to scrape: ')
    data_type = input('What data would you like to scrape (e.g., images, audio, headlines, products, jobs)?: ')
    save_format = input('How would you like to save the data? (csv/database): ')
    
    scrape_data(url, data_type, save_format)

if __name__ == "__main__":
    main()
