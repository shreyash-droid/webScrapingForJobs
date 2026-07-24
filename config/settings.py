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

    # Job Preferences
    # Keywords matched against the job TITLE to decide relevance (case-insensitive).
    # Covers UI/UX & Product Design, Frontend Engineering, and Product Management.
    TARGET_ROLES = [
        "designer", "ux", "ui", "product design", "product designer",
        "frontend", "front end", "front-end", "web developer",
        "product manager", "associate product manager", "apm",
    ]
    # Titles containing any of these are dropped outright.
    EXCLUDE_KEYWORDS = ["game", "gaming", "unity", "unreal", "backend", "devops", "sales"]

    # Experience Level
    # Entry-level signals. Used to keep/boost early-career roles.
    EXPERIENCE_KEYWORDS = [
        "intern", "internship", "junior", "jr ", "jr.", "entry level", "entry-level",
        "graduate", "new grad", "trainee", "apprentice",
        "0-1 year", "0-2 year", "1 year", "no experience", "early career",
    ]
    # Seniority signals. Titles containing these are dropped (too senior).
    SENIOR_KEYWORDS = [
        "senior", "sr.", "sr ", "lead", "principal", "staff", "architect",
        "director", "head of", "vp ", "manager of", "mid-level", "mid level",
        "group product manager", "l3", "l4", "l5", "level iii", "level iv",
        "2+ years", "3+ years", "4+ years", "5+ years", "6+ years",
        "7+ years", "8+ years", "10+ years",
    ]
    # When True, keep ONLY roles with an explicit entry-level signal.
    # When False (default), also keep roles with no seniority signal at all
    # (ambiguous titles), letting the scorer rank explicit entry-level roles higher.
    STRICT_ENTRY_LEVEL = False

    # We Work Remotely RSS category feeds.
    WWR_FEEDS = [
        "remote-design-jobs",
        "remote-front-end-programming-jobs",
        "remote-product-jobs",
    ]

    # Sources considered "High Quality/Genuine" (bonus scoring)
    GENUINE_SOURCES = ["WeWorkRemotely", "Remotive", "RemoteOK"]

settings = Settings()
