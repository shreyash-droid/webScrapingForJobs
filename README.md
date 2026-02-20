# Job Automation System

A production-ready, modular Python system for internship and job scraping automation.

## Project Structure

```text
project/
│── main.py             # Entry point
│── scraper/            # Scraper modules
│   └── base_scraper.py # Abstract base class
│── utils/              # Utility functions
│   ├── logger.py       # Central logging
│   └── google_sheets.py # Sheets integration
│── config/             # Configuration management
│   └── settings.py     # Environment settings
│── .env                # Environment variables (sensitive)
│── .gitignore          # Git exclusion rules
│── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Prerequisite: Python 3.10+
Ensure you have Python 3.10 or higher installed.

### 2. Install Dependencies
Run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
Playwright requires browser binaries to function. Install them using:

```bash
python -m playwright install
```

### 4. Configuration
1. Rename/Update the `.env` file with your credentials.
2. Place your Google Service Account JSON file in `config/credentials.json`.
3. Update `SPREADSHEET_ID` in `.env`.

### 5. Run the System
Start the automation system:

```bash
python main.py
```

## Adding New Scrapers
To add a new scraper, create a new file in the `scraper/` directory that inherits from `BaseScraper` in `scraper/base_scraper.py`.
