import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "config/credentials.json")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
    SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL_MINUTES", 60))

config = Config()
