# Underdog Fantasy Sports Scraper

This project provides a Python script to scrape and process pickem data from Underdog Fantasy Sports and output the results to a CSV file.

## Description

The Underdog Scraper is designed to:
1. Fetch data from Underdog Fantasy Sports API
2. Process and combine different data sets (players, appearances, over/under lines)
3. Apply name corrections if necessary
4. Filter and clean the data
5. Export the processed data to a CSV file

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/underdog-scraper.git
   cd underdog-scraper
   ```

2. Install the required Python packages:
   ```
   pip install requests pandas
   ```

3. Ensure you have a `config.json` file in the same directory as the script with the necessary configuration (API URL and headers). You should not have to edit this file, unless Underdog changes their API endpoints.

## Usage

1. Open the `underdog_scraper.py` file.

2. Uncomment the last two lines of the script:
   ```python
   scraper = UnderdogScraper()
   scraper.scrape()
   ```

3. Run the script:
   ```
   python underdog_scraper.py
   ```

4. The script will fetch data and save the results to `underdog_props.csv` in the same directory.

## FAQ

If you have comments or questions reach out to me on Twitter/X @tistonionwings

## Donation

If you find this project helpful and would like to support the developer, you can donate to the following BTC address:

bc1q9s5q6wy3ntumpsel834axwf6x55up4uvk3uyr0

Thank you for your generosity!
