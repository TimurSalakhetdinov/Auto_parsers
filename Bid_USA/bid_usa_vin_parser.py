import os  # Add this import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from datetime import datetime
from random import randint
import traceback

def bid_parser(limit=None):
    collected = 0
    current_page = 1
    max_pages = 500  # Maximum number of pages to scrape
    max_collected = limit if limit is not None else float('inf')  # If no limit is set, scrape all records
    offers = []
    batch_size = 1000  # Save records in batches of 1000
    batch_count = 1  # Counter for batch files

    # Get the directory of the current Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while collected < max_collected and current_page <= max_pages:
        options = webdriver.ChromeOptions()
        # Comment out the headless line to debug visually
        #options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)

        try:
            # Navigate to the current page
            URL = f"https://bid.cars/ru/automobile/page/{current_page}"
            print(f"Scraping page {current_page}...")
            driver.get(URL)

            # Debug: Allow time for dynamic content to load
            sleep(5)

            # Wait for VIN elements to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.vin_title > a"))
            )

            # Extract all VINs from the current page
            vin_elements = driver.find_elements(By.CSS_SELECTOR, "h2.vin_title > a")

            if not vin_elements:
                print(f"No VIN elements found on page {current_page}. Exiting...")
                break

            # Process all VINs on the page
            for vin_element in vin_elements:
                if collected >= max_collected:
                    break

                try:
                    vin = vin_element.text.strip()

                    # Debug: Print extracted VIN
                    #print(f"Extracted VIN: {vin}")

                    # Append to the offers list
                    offers.append({"VIN": vin})
                    collected += 1

                    # Save batch of records
                    if len(offers) >= batch_size:
                        save_to_csv(offers, batch_count, script_dir)
                        offers.clear()
                        batch_count += 1

                except Exception as e:
                    print(f"Error processing VIN element: {e}")
                    traceback.print_exc()

            # Move to the next page
            current_page += 1
            sleep(randint(2, 5))  # Randomized delay to mimic human behavior

        except Exception as e:
            print(f"Error on page {current_page}: {e}")
            traceback.print_exc()

        finally:
            driver.quit()

    # Save any remaining records
    if offers:
        save_to_csv(offers, batch_count, script_dir)

    print(f"Scraped {collected} records in total.")


def save_to_csv(offers, batch_number, output_dir):
    """
    Save a list of VINs to a CSV file in the same directory as the script.
    """
    df = pd.DataFrame(offers)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'bid_offers_{date_str}_batch_{batch_number}.csv'
    file_path = os.path.join(output_dir, filename)  # Save in the same directory
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Saved {len(offers)} records to {filename}")


if __name__ == "__main__":
    bid_parser(limit=None)  # Set limit=None to scrape all available VINs
    print("Scraping complete.")