from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
from datetime import datetime
from random import randint
import traceback

# Function to save the scraped data to a CSV file
def save_to_csv(offers, batch_number):
    df = pd.DataFrame(offers)
    date_str = datetime.now().strftime("%Y-%m-%d")  # Format the date as YYYY-MM-DD
    filename = f'americanmotors_{date_str}_{batch_number}.csv'  # Append the date and batch number to the filename
    df.to_csv(filename, index=False)

# Function to parse the americanmotors website
def americanmotors_parser(limit=None, csv_limit=1000):
    collected = 0
    batch_number = 1
    offers = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)

    try:
        URL = "https://americamotors.com/auction/car"
        print("Navigating to URL...")
        driver.get(URL)
        print("Waiting for car elements...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.catalog__transport.transport.transport_buy .transport__row')))
        sleep(randint(2, 5))

        while True:
            car_elements = driver.find_elements(by=By.CSS_SELECTOR, value='.catalog__transport.transport.transport_buy .transport__row')
            if not car_elements:
                print("No cars found on the page. Ending scraping process.")
                break  # No car elements found on the page, break the loop

            car_urls = [elem.find_element(by=By.CSS_SELECTOR, value='a.transport__name').get_attribute("href") for elem in car_elements]

            for car_url in car_urls:
                if limit and collected >= limit:
                    break

                vin = car_url.rsplit('/', 1)[-1]
                offers.append({"URL": car_url, "VIN": vin})
                collected += 1

                if collected % csv_limit == 0:
                    save_to_csv(offers, batch_number)
                    print(f"Processed {collected} cars")
                    offers = []  # Reset the offers list after saving
                    batch_number += 1

            if collected >= limit if limit else float('inf'):
                break  # Limit reached, break the loop

            # Code to navigate to the next page
            try:
                # Wait for the 'Next' button to be clickable
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagination__link.page-link[wire\\:click="nextPage"]'))
                )
                
                # Scroll to the 'Next' button
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                sleep(1)  # Allow time for scrolling

                # Click the 'Next' button
                next_button.click()

                # Wait for the next page to load completely
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.catalog__transport.transport.transport_buy .transport__row'))
                )
                sleep(randint(2, 5))  # Random delay to mimic human behavior

            except (ElementClickInterceptedException, NoSuchElementException) as e:
                print("Could not click 'Next' button or 'Next' button not found. Ending scraping process.")
                break
            except TimeoutException:
                print("Timed out waiting for page to load. Ending scraping process.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        if offers:  # Save any remaining offers before quitting
            save_to_csv(offers, batch_number)
        driver.quit()

    print("Scraping complete.")

if __name__ == "__main__":
    offers = americanmotors_parser(limit=200000)  # Set the limit as per your requirement
