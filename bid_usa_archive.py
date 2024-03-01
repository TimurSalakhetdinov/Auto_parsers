from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pandas as pd
import re
from datetime import datetime
from random import randint
import traceback

URL = f"https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=1900&year-to=2025&make=All&model=All&auction-type=All"

# Function to parse the Avito website
def bid_parser(limit=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    driver.get(URL)
    
    offers = []
    collected = 0

    while True:
        elems = driver.find_elements(by=By.CSS_SELECTOR, value="div.items-row.archived-result")
        for elem in elems:
            if limit and collected >= limit:
                break

            try:
                auto_id = elem.find_element(by=By.CSS_SELECTOR, value='.item-horizontal.lots-search').get_attribute("id")
                
                # Find the element with class 'damage-info'
                damage_info_element = elem.find_element(By.CSS_SELECTOR, ".damage-info")
                damage_info_text = damage_info_element.text if damage_info_element else ""
                damage_info_text = damage_info_text.split(',')[0]

                # Use regular expression to separate year and model
                match = re.search(r'(\d{4})\s+(.*)', damage_info_text)
                if match:
                    year = match.group(1)  # This is the year
                    model = match.group(2)  # This is the model
                else:
                    year = "Year not found"
                    model = "Model not found"

                # Find VIN number
                li_element = elem.find_element(By.XPATH, ".//li[contains(@class, 'no-wrap-text-ellipsis')]")
                li_text = li_element.get_attribute("textContent")
                vin_match = re.search(r'VIN:\s*(\w+)', li_text)
                if vin_match:
                    vin = vin_match.group(1)
                else:
                    vin = "No VIN"

                today = datetime.now().date()

                result = {
                    "ID": auto_id,
                    "VIN": vin,
                    "Model": model,
                    "Year": year,
                    "Today": today,
                }
                offers.append(result)
                collected += 1

            except Exception as e:
                print(f"An error occurred at {collected}: {e}")
                traceback.print_exc()

        if limit and collected >= limit:
            break

        # Increment the page number for the next iteration
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a[data-next-page]")
            driver.execute_script("arguments[0].click();", next_button)
            sleep(randint(5, 10))  # Sleep to allow page to load; adjust as necessary.

        except NoSuchElementException:
            print("No more pages to parse.")
            break
    
    driver.quit()
    
    save_to_excel(offers)

    return offers

def save_to_excel(offers):
    df = pd.DataFrame(offers)
    date_str = datetime.now().strftime("%Y-%m-%d")  # Format the date as YYYY-MM-DD
    filename = f'bid_offers_archive_{date_str}.xlsx'  # Append the date to the filename
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    offers = bid_parser(limit=10)
    print("Scraping complete.")