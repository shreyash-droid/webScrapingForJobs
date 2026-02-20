import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIAL_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIAL_FILE", "config/credentials.json")
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

    # Scraper
    SCRAPE_INTERVAL_MINUTES = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "60"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

settings = Settings()
