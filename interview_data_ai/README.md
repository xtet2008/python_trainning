# College Scraper

This project contains a simple web scraper that extracts a list of colleges from the College Board website and saves the data to JSON files.

## Files

- `scraper_for_interview.py`: The main Python script that performs the scraping.
- `college_list.json`: A JSON file containing the list of all colleges.
- `massachusetts_institute_of_technology.json`: A JSON file containing data for MIT.
- `harvard_college.json`: A JSON file containing data for Harvard College.
- `Makefile`: A file to automate running the scraper and cleaning up generated files.
- `README.md`: This README file.

## Requirements

- Python 3  # version: >= 3.8
- `aiohttp` package
- `asyncio` package
- `BeautifulSoup` package



## Setup

1. Install the required packages:
    ```sh
    pip install requests aiohttp
    pip install requests asyncio
    pip install requests beautifulsoup4
    ```

2. Run the scraper:
    ```sh
    # To run the scraper and generate the JSON files:
    make scrape 
   
    # To clean up the generated JSON files:
    make clean
    ```

The scraper will fetch the list of colleges from the College Board website and save it to `college_list.json`. It will also save additional data for MIT and Harvard College in separate JSON files.
