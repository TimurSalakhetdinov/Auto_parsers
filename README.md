# Vehicle Data Scraping Tools

This repository hosts a collection of Python scripts designed for scraping vehicle data from various online platforms. Each tool is tailored to a specific website, allowing users to extract detailed information about vehicles listed for auctions or sales.

## Featured Scripts

- **Bid Cars Web Scraper**: Extracts auction data from the Bid Cars website, including vehicle IDs, VINs, models, years, and URLs. Data can be saved to Excel or a SQLite database.

- **American Motors Scraper**: Gathers vehicle information from the American Motors website. It focuses on VINs and URLs of the vehicles listed for sale.

## General Features

- Automated navigation through website pages to collect vehicle data.
- Customizable limits for the number of items to scrape.
- Data export options include Excel files and SQLite databases.
- Built with Selenium for dynamic content handling.

## Installation

Clone the repository and install required dependencies as specified in each script's documentation. Ensure you have Python 3.x and Selenium WebDriver installed.

```bash
git clone <repository-url>
cd <specific-scraper-folder>
pip install -r requirements.txt
```

## Usage

Navigate to the directory of the scraper you wish to use and follow the instructions in the respective README files for detailed usage guidelines.

## Contributing

Contributions, suggestions, and improvements are welcome. Please refer to the contributing guidelines in each scraper's folder for more information.

## Disclaimer

These scripts are intended for educational and research purposes only. Users are responsible for complying with the terms of use of the websites they are scraping and for any consequences of their scraping activities.

## License

The tools in this repository are provided under an open license for educational use. The authors are not liable for any misuse or damage.