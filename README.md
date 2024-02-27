# **Bid Cars Web Scraper**

## Overview

This repository contains a Python script for scraping vehicle auction data from the "bid.cars" website. The script navigates through the auction pages, collects information on each vehicle, and saves the data either to an Excel file or a SQLite database, based on user preference.

## Features

- Scrapes vehicle details such as ID, VIN, model, year, and URL.
- Option to limit the number of items collected.
- Data can be saved to an Excel file or a SQLite database.
- Implements Selenium for web scraping to handle dynamic content.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Selenium WebDriver
- pandas
- openpyxl (for Excel file handling)
- SQLite3 (for database handling)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bid-cars-scraper.git
```

2. Navigate to the project directory:
```bash
cd bid-cars-scraper
```

3. Install the required Python packages:
```
pip install -r requirements.txt
```

## Usage

To run the script, execute the following command in your terminal:
```
python bid_parser.py
```

### Script Arguments

- limit (optional): Sets the maximum number of vehicles to scrape. If not set, the script will continue until there are no more pages left to scrape.
- save_to_db (optional): If set, the script will save the data to a SQLite database. Otherwise, data will be saved to an Excel file by default.

### Example Command
```
python bid_parser.py --limit 100 --save_to_db
```

This command will scrape data for 100 vehicles and save the information to a SQLite database.

## Output

- The Excel file will be named in the format bid_offers_YYYY-MM-DD.xlsx and saved in the project directory.
- The SQLite database will be named bid_cars.db and also saved in the project directory.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or improvements.

## Acknowledgements

Thanks to the Selenium project for providing the tools necessary for web scraping dynamic websites.