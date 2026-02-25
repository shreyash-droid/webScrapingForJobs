# CareerBot: Automated Job Search & Tracking Pipeline

A production-grade Python automation system designed to streamline the job hunt by aggregating, filtering, and prioritizing opportunities from multiple platforms. Developed with a focus on **UI/UX, Product, and Frontend** roles.

## 🚀 Overview

CareerBot automates the entire lifecycle of job discovery:
1.  **Distributed Scraping**: Aggregates listings from Indeed, Wellfound (AngelList), YC Jobs, RemoteOK, Remotive, and WeWorkRemotely.
2.  **Intelligent Filtering**: Uses regex-based natural language processing to isolate relevant roles while filtering out boilerplate and IR (e.g., Game Design exclusion).
3.  **Priority Scoring Engine**: A custom ranking algorithm that scores jobs based on:
    *   **Visa Sponsorship** (+3)
    *   **Remote Status** (+2)
    *   **Startup/Tier-1 Source** (+1)
    *   **Role Match Density** (+1)
4.  **Real-time Alerts**: Pushes high-priority "Top 10" matches directly to a Telegram mobile bot.
5.  **Cloud Sync**: Synchronizes all findings to a centralized Google Sheets tracker for long-term application management.

## 🛠️ Tech Stack

*   **Logic**: Python 3.11+
*   **Automation**: Playwright (Headless Browser Orchestration)
*   **Data Science**: Pandas (Data cleaning, normalization, and deduplication)
*   **Integrations**: Google Sheets API (gspread), Telegram Bot API
*   **DevOps**: Python-Schedule, Windows Task Scheduler / Cron support

## 📂 Project Structure

```text
├── config/
│   ├── settings.py      # Pydantic-style configuration management
│   └── credentials.json # Google Cloud Service Account (Git-ignored)
├── scraper/
│   ├── base_scraper.py  # Abstract base class for extensible scraping
│   ├── indeed.py        # High-volume Indeed integration
│   ├── wellfound.py     # Anti-bot resilient scraper for AngelList
│   └── ... (other sources)
├── utils/
│   ├── filter.py        # NLP-based role filtering
│   ├── scoring.py       # Priority ranking algorithm
│   ├── sheets.py        # Cloud-sync and deduplication logic
│   └── notifier.py      # Telegram notification service
└── main.py              # Orchestration entry point
```

## ⚙️ Setup & Installation

### 1. Prerequisites
* Python 3.11 or higher
* A Telegram Bot Token (via @BotFather)
* A Google Cloud Service Account JSON key

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_SHEETS_KEY=your_sheet_id
SCRAPE_INTERVAL_MINUTES=60
```

### 3. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/CareerBot.git
cd CareerBot

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### 4. Running the System
```bash
python main.py
```

## 📈 Features for Resume Showcase

*   **Architecture**: Implemented using the **Strategy Pattern** for scrapers, ensuring the system is highly extensible (adding a new site takes < 15 minutes).
*   **Resilience**: Robust error handling ensures that if one job board is down, the entire pipeline remains operational.
*   **Deduplication**: Multi-layered deduplication logic prevents redundant entries across different sources and historical cloud data.
*   **Automation**: Configured for 24/7 autonomous operation with scheduled daily scans.

---
*Created as a high-performance tool for modern designers and developers.*
