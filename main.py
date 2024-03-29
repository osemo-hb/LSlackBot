from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def fetch_listings(url):
    """Fetches listings from a dynamically loaded website using Selenium."""
    driver = webdriver.Chrome()

    driver.get(url)
    
    time.sleep(10) # sleep time.
    
    # Efficiently locate element containing shoe data, using CSS selector logic.
    a_tags = driver.find_elements(By.CSS_SELECTOR, '.feed-grid__item a.new-item-box__overlay.new-item-box__overlay--clickable')
    
    filtered_data = []
    for a_tag in a_tags:
        title = a_tag.get_attribute('title')
        
        if 'hinta' in title:
            try:
                price_info = title.split('hinta:')[1].split(',')[0].strip()
                price = price_info.replace('\xa0€', '').replace('.', '').replace(',', '.').strip()
                price_float = float(price)
                
                # Filtering by price
                if price_float <= 20:
                    href = a_tag.get_attribute('href')
                    filtered_data.append({'title': title, 'price': price_float, 'url': href})
            except (IndexError, ValueError):
                continue
    
    driver.quit()
    return filtered_data

url = 'https://www.vinted.fi/catalog?search_text=air%20force%201&search_id=13883589529&color_ids[]=12&currency=EUR'
listings_data = fetch_listings(url)
for listing in listings_data:
    print(listing)
