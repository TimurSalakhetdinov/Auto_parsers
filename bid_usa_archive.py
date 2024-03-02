from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import re
from datetime import datetime

def bid_parser(limit=None):
    URL = "https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=1900&year-to=2025&make=All&model=All&auction-type=All"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    driver.get(URL)
    
    collected = 0
    offers = []
    file_index = 1
    
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.items-row.archived-result > div.item-horizontal.lots-search"))
        )
        car_elements = driver.find_elements(By.CSS_SELECTOR, "div.items-row.archived-result > div.item-horizontal.lots-search")
        
        for car_elem in car_elements:
            if limit and collected >= limit:
                save_to_csv(offers, file_index)
                return offers
            
            auto_id = car_elem.get_attribute("id")
            url = car_elem.find_element(by=By.CSS_SELECTOR, value='.item-title a').get_attribute("href")

            damage_info_element = car_elem.find_element(By.CSS_SELECTOR, ".damage-info")
            damage_info_text = damage_info_element.text.split(',')[0] if damage_info_element else ""
            
            year, model = (match.groups() if (match := re.search(r'(\d{4})\s+(.*)', damage_info_text)) else ("Year not found", "Model not found"))
            
            li_element = car_elem.find_element(By.XPATH, ".//li[contains(@class, 'no-wrap-text-ellipsis')]")
            li_text = li_element.get_attribute("textContent")
            vin = (vin_match.group(1) if (vin_match := re.search(r'VIN:\s*(\w+)', li_text)) else "No VIN")
            
            today = datetime.now().date()
            offers.append({
                "ID": auto_id,
                "VIN": vin,
                "Model": model,
                "Year": year,
                "Today": today,
                "URL": url, 
            })
            collected += 1
        
            if len(offers) >= 100000:
                save_to_csv(offers, file_index)
                offers = []  # Reset the offers list after saving
                file_index += 1  # Increment the file index for next save
        
        if limit and collected >= limit:
            break
        
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-next-page]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
        except (TimeoutException, NoSuchElementException):
            print("No more pages to parse or button not clickable.")
            break
    
    driver.quit()

    if offers:  # Save any remaining data that was not written to a file
        save_to_csv(offers, file_index)
    return offers

def save_to_csv(offers, index):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'bid_offers_{date_str}_{index}.csv'
    df = pd.DataFrame(offers)
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")

if __name__ == "__main__":
    offers = bid_parser(limit=1000000)  # Adjust the limit as necessary
    print("Scraping complete.")
