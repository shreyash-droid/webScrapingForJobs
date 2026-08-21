# CareerBot: Automated Job Search & Tracking Pipeline

A Python automation pipeline that aggregates remote job listings from multiple
sources, filters them down to entry-level design / frontend / product roles,
scores and ranks them, pushes the top matches to Telegram, and syncs new
listings to a Google Sheets tracker.

## 🚀 Overview

CareerBot runs a repeatable cycle: **Scrape → Filter → Score/Dedup → Notify → Sync**

1. **Multi-source aggregation** — pulls listings from RemoteOK, Remotive, and
   We Work Remotely over their public JSON APIs and RSS feeds (no headless
   browser required).
2. **Two-stage relevance filtering** — a required title match against target
   roles, followed by dropping only *explicitly* senior roles. Ambiguous
   titles are kept and left for the scorer to rank, so nothing relevant is
   silently discarded.
3. **Weighted scoring engine** — each job is scored on:
   * **Visa sponsorship / relocation** (+3)
   * **Remote status** (+2)
   * **Genuine source** (+2)
   * **Entry-level signal** (+3 in title, +1 in body)
   * **Startup signal** (+1)

   Scores are bucketed into `High` (≥6), `Medium` (≥3), and `Low`.
4. **Multi-layer deduplication** — cross-source dedup on a normalized
   `company + role` key, plus link-based dedup against jobs already in the
   sheet.
5. **Real-time alerts** — sends the top 10 matches to a Telegram bot.
6. **Cloud sync** — appends only new listings to a Google Sheets tracker for
   long-term application management.

## 🛠️ Tech Stack

* **Language**: Python 3.11+
* **HTTP / parsing**: `requests`, `xml.etree.ElementTree` (RSS)
* **Data**: Pandas (normalization, deduplication, ranking)
* **Integrations**: Google Sheets API (`gspread` + `oauth2client`), Telegram Bot API
* **Scheduling**: `schedule` (pure-Python, cross-platform)

> **Design note:** the pipeline fetches structured data over plain HTTP/RSS
> rather than driving a headless browser. This is faster, avoids anti-bot
> friction, and returns real job descriptions to filter and score against.

## 📂 Project Structure

```text
├── config/
│   └── settings.py          # Env-driven configuration & role/keyword lists
├── scraper/
│   ├── base_scraper.py      # Abstract base (Strategy + Template Method)
│   ├── remoteok.py          # RemoteOK public JSON API
│   ├── remotive.py          # Remotive public JSON API
│   └── weworkremotely.py    # We Work Remotely category RSS feeds
├── utils/
│   ├── filter.py            # Two-stage relevance filtering
│   ├── scoring.py           # Weighted scoring + local deduplication
│   ├── sheets.py            # Google Sheets sync + cloud deduplication
│   ├── notifier.py          # Telegram notification service
│   └── logger.py            # Console + file logging
└── main.py                  # Orchestration entry point
```

## ⚙️ Setup & Installation

### 1. Prerequisites
* Python 3.11 or higher
* A Telegram Bot Token (via @BotFather) and your chat ID
* A Google Cloud service-account JSON key with Sheets/Drive access

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
SPREADSHEET_ID=your_google_sheet_id
GOOGLE_SHEETS_CREDENTIAL_FILE=config/credentials.json
SCRAPE_INTERVAL_MINUTES=60
LOG_LEVEL=INFO
```
Place your service-account key at `config/credentials.json` (git-ignored).

### 3. Installation
```bash
git clone https://github.com/yourusername/CareerBot.git
cd CareerBot
pip install -r requirements.txt
```

### 4. Running the System
```bash
python main.py
```
The pipeline runs one cycle immediately, then schedules a daily run at 10:00.

## 🧩 Architecture Highlights

* **Strategy + Template Method** — every source subclasses `BaseScraper` and
  implements only `scrape()`; the base `run()` wraps it with error handling so
  one failing source can't crash the cycle. Adding a new source is a single
  new subclass, with no changes to the orchestrator.
* **Fault isolation** — errors are contained at both the scraper and
  orchestrator level; the pipeline degrades gracefully when a source is down.
* **Deduplication** — local (normalized company+role) and cloud-side
  (link already present in the sheet) layers keep the tracker clean across
  runs and sources.
* **Idempotent sync** — re-running a cycle never creates duplicate sheet rows.

## 🔭 Possible Improvements

* Parallelize scrapers with `asyncio` / a thread pool.
* Retry-with-backoff and rate-limit handling in `fetch()`.
* Unit tests for `is_relevant()` and `calculate_score()` (pure functions).
* Move persistence from Sheets to a database with a unique index for O(1) dedup.
