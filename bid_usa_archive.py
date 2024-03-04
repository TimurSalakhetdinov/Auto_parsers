from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import pandas as pd
import re

def save_to_csv(offers, index):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'bid_offers_{date_str}_{index}.csv'
    df = pd.DataFrame(offers)
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")

def bid_parser(total_limit=None, iteration_limit=None):
    """
    Scrapes car data from the specified URL and saves it to CSV files, each containing up to 'iteration_limit' records.
    Continues scraping until 'total_limit' records are collected or no more data is available.

    Arguments:
    total_limit -- (Optional) The total number of records to scrape. If None, scraping continues until no more data is available.
    iteration_limit -- (Optional) The maximum number of records to include in each CSV file before starting a new one. Defaults to 50000.

    Returns:
    None -- This function saves the scraped data to CSV files and does not return any value.
    """
        
    base_url = "https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=1900&year-to=2025&make=All&model=All&auction-type=All"
    PROXY = "136.243.82.121:1082"
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    options.add_argument(f'--proxy-server={PROXY}')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    driver.set_script_timeout(30)
    
    driver.get(base_url)
    
    collected = 0
    offers = []
    file_index = 1
    batch_collected = 0  # Reset batch counter

    while (not total_limit or collected < total_limit):
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.items-row.archived-result > div.item-horizontal.lots-search"))
        )
        car_elements = driver.find_elements(By.CSS_SELECTOR, "div.items-row.archived-result > div.item-horizontal.lots-search")
        
        if not car_elements:
            print("No car elements found on the page. Ending scrape.")
            break

        for car_elem in car_elements:
            if total_limit and collected >= total_limit:
                break
            
            auto_id = car_elem.get_attribute("id")
            #url = car_elem.find_element(By.CSS_SELECTOR, '.item-title a').get_attribute("href")

            damage_info_element = car_elem.find_element(By.CSS_SELECTOR, ".damage-info")
            damage_info_text = damage_info_element.text.split(',')[0] if damage_info_element else ""
            
            year, model = (match.groups() if (match := re.search(r'(\d{4})\s+(.*)', damage_info_text)) else ("Year not found", "Model not found"))
            
            li_element = car_elem.find_element(By.XPATH, ".//li[contains(@class, 'no-wrap-text-ellipsis')]")
            li_text = li_element.get_attribute("textContent")
            vin = (vin_match.group(1) if (vin_match := re.search(r'VIN:\s*(\w+)', li_text)) else "No VIN")
            
            #today = datetime.now().date()
            
            offers.append({
                "ID": auto_id,
                "VIN": vin,
                "Model": model,
                "Year": year,
                #"Today": today,
                #"URL": url, 
            })
            
            batch_collected += 1
            collected += 1

            # Save batch if iteration_limit is set and reached
            if iteration_limit is not None and batch_collected >= iteration_limit:
                save_to_csv(offers, file_index)
                offers = []  # Reset the offers list after saving
                file_index += 1  # Increment the file index for next save
                batch_collected = 0  # Reset batch counter

        if total_limit and collected >= total_limit:
            break
        
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-next-page]"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.unique-element-on-next-page"))
    )

        except (TimeoutException, NoSuchElementException):
            print("No more pages to parse or button not clickable.")
            break

    if offers:  # Save any remaining data that was not written to a file
        save_to_csv(offers, file_index)
    
    driver.quit()

if __name__ == "__main__":
    offers = bid_parser(total_limit=150, iteration_limit=None)  # Adjust the limits as necessary
    print("Scraping complete.")