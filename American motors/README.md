# American Motors Scraper

## Overview
This Python script is designed to scrape vehicle data from the American Motors website. It navigates through the vehicle listings, extracting information such as the Vehicle Identification Number (VIN) and the URL for each listed car.

## Requirements
- Python 3.x
- Selenium WebDriver
- ChromeDriver (or any compatible driver for your browser of choice)
- Pandas

## Installation
1. Ensure you have Python installed on your machine.
2. Install Selenium and Pandas using pip:

```
pip install selenium pandas
```

3. Download the ChromeDriver (or corresponding driver for your browser) and ensure it's in your PATH.

## Usage
Run the script from the command line, specifying the limit for the number of cars you want to scrape:

```
python americanmotors_parser.py --limit 100
```

If the `--limit` argument is omitted, the script will attempt to scrape data for all available cars on the website.

### Usage

Adjust the `csv_directory` variable in the script to point to the folder containing your CSV files and run the script. The combined file will be saved in the same directory.

This is a convenient way to aggregate data from multiple scraping sessions into a unified dataset for analysis or storage.

## Features
- **Headless Scraping**: Runs in headless mode to improve performance.
- **Pagination Handling**: Automatically navigates through pages of car listings.
- **Error Handling**: Gracefully handles errors and exceptions, ensuring the scraper can run unattended.
- **Data Export**: Automatically saves the scraped data into CSV files, each containing up to 500 records.

## Output
The script outputs CSV files with the scraped data. Each file is named in the format `americanmotors_YYYY-MM-DD_batchnumber.csv`, where `YYYY-MM-DD` is the date when the data was scraped, and `batchnumber` is a sequential number starting from 1 for each set of 500 cars.

## Customization
You can modify the `csv_limit` parameter in the `americanmotors_parser` function to change the number of records per CSV file.

## Combining CSV Files

If you have multiple CSV files from the American Motors scraper and wish to combine them into a single file, follow these steps:

1. Ensure all CSV files are in the same directory.
2. Use the provided Python script `combine_csv.py` to merge these files. The script reads all CSV files matching the pattern `americanmotors_YYYY-MM-DD_*.csv` and combines them into a single file named `americanmotors_YYYY-MM-DD.csv`.

## Note
Ensure that you comply with the American Motors website's terms of use and scraping policies before using this script.

## License
This script is provided for educational purposes only. The author is not responsible for any misuse or damage resulting from the use of this script.