from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import re
import requests
import json
import os

def initialize_driver(): # Initialize the Selenium WebDriver for headless execution on Raspberry Pi
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage') 
    try:
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        return None

def has_been_posted(url, filepath='posted_listings.txt'): # Check if the listing has already been posted by checking against a file
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r') as file:
        posted_urls = file.read().splitlines()
    return url in posted_urls

def mark_as_posted(url, filepath='posted_listings.txt'): # Mark a listing as posted by adding its URL to a file
    with open(filepath, 'a') as file:
        file.write(url + '\n')

def post_to_slack(webhook_url, listing): # Posts a single listing to a Slack channel.
    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{listing['url']}|{listing['title']}>*\nPrice: {listing['price']}€"
                },
                "accessory": {
                    "type": "image",
                    "image_url": listing['img_src'],
                    "alt_text": "product image"
                }
            }
        ]
    }
    response = requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        print(f"Error posting to Slack: {response.text}")

def fetch_listings(url, start_page=1, end_page=2):
    driver = initialize_driver()
    filtered_data = []
    max_listings = 10000  # for safety in case of a catastrophic error and infinite runtime

    try:
        listing_count = 0
        for page in range(start_page, end_page + 1):
            if listing_count >= max_listings:
                break 

            updated_url = f"{url}&page={page}"
            print(f"Fetching {updated_url}")

            driver.get(updated_url)

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.feed-grid__item')))
            items = driver.find_elements(By.CSS_SELECTOR, '.feed-grid__item a.new-item-box__overlay.new-item-box__overlay--clickable')

            for item in items:
                if listing_count >= max_listings:
                    break 

                title = item.get_attribute('title').lower()
                href = item.get_attribute('href')

                if not has_been_posted(href):
                    try:
                        parent_div = item.find_element(By.XPATH, './..')
                        img_element = parent_div.find_element(By.CSS_SELECTOR, 'img')
                        img_src = img_element.get_attribute('src')
                    except NoSuchElementException:
                        img_src = 'https://via.placeholder.com/150'

                    if re.search(r'word1|word2', title): # continue scraping if either word1 or word2 is part of the title.
                        price_info = re.search(r'hinta: (\d+,\d+)', title)
                        if price_info:
                            price = price_info.group(1).replace(',', '.')
                            price_float = float(price)

                            if price_float <= 15:
                                filtered_data.append({'title': title, 'price': price_float, 'url': href, 'img_src': img_src})
                                mark_as_posted(href)
                                listing_count += 1 

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()

    return filtered_data

webhook_url = ''
url = ''
listings_data = fetch_listings(url, 1, 7)
for listing in listings_data[:10000]:
    post_to_slack(webhook_url, listing)



