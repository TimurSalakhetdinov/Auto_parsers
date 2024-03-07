from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pandas as pd
import re
import sqlite3
from datetime import datetime
from random import randint
import traceback

# Function to parse the Avito website
def bid_parser(limit=None, save_to_db=False):
    collected = 0
    current_page = 1
    max_collected = limit if limit is not None else float('inf')
    offers = []

    while collected < max_collected:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(15)

        # Construct the URL for the current page and navigate to it
        URL = f"https://bid.cars/ru/automobile/page/{current_page}"
        driver.get(URL)

        elems = driver.find_elements(by=By.CSS_SELECTOR, value='div.items-row')
        
        for elem in elems:
            if limit and collected >= limit:
                break

            try:
                auto_id = elem.find_element(by=By.CSS_SELECTOR, value='.item-horizontal.lots-search').get_attribute("id")
                url = elem.find_element(by=By.CSS_SELECTOR, value='.item-title a').get_attribute("href")
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
                    "URL": url,
                }
                offers.append(result)
                collected += 1

            except Exception as e:
                print(f"An error occurred at {collected}: {e}")
                traceback.print_exc()

        # Close the browser window after scraping the page
        driver.quit()

        if collected >= max_collected:
            break

        # Increment the page number for the next iteration
        current_page += 1
        sleep(randint(2, 5))  # Sleep to allow page to load; adjust as necessary.

    if save_to_db:
        save_to_database(offers)
    else:
        save_to_excel(offers)

    return offers

def save_to_excel(offers):
    df = pd.DataFrame(offers)
    date_str = datetime.now().strftime("%Y-%m-%d")  # Format the date as YYYY-MM-DD
    filename = f'bid_offers_{date_str}.xlsx'  # Append the date to the filename
    df.to_excel(filename, index=False)

def save_to_database(offers):
    conn = sqlite3.connect('bid_cars.db')
    c = conn.cursor()
    # Create the table with the matching columns
    c.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            ID INTEGER PRIMARY KEY,
            Model TEXT,
            Year INTEGER,
            Power INTEGER,
            Price INTEGER,
            Region TEXT,
            Time TEXT,
            Today DATE,
            URL TEXT
        )
    ''')

    # Insert data into the table
    for offer in offers:
        c.execute('''
            INSERT INTO cars (ID, Model, Year, Power, Price, Region, Time, Today, URL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            offer["ID"], 
            offer["Model"], 
            offer["Year"], 
            offer["Power"], 
            offer["Price"], 
            offer["Region"], 
            offer["Time"], 
            offer["Today"], 
            offer["URL"]
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    offers = bid_parser(limit=25, save_to_db=False)
    print("Scraping complete.")