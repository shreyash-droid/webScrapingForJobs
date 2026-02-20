import schedule
import time
import sys
import pandas as pd
from typing import List

from config.settings import settings
from utils.logger import logger
from utils.sheets import tracker
from utils.filter import job_filter
from utils.scoring import job_scorer
from utils.notifier import notifier

# Scrapers
from scraper.remoteok import RemoteOKScraper
from scraper.remotive import RemotiveScraper
from scraper.weworkremotely import WeWorkRemotelyScraper
from scraper.wellfound import WellfoundScraper
from scraper.yc_jobs import YCJobsScraper
from scraper.base_scraper import BaseScraper

class JobAutomationOrchestrator:
    """
    Orchestrates the job automation pipeline:
    Scrape -> Combine -> Filter -> Score -> Notify -> Sync
    """
    
    def __init__(self):
        self.scrapers: List[BaseScraper] = [
            RemoteOKScraper(),
            RemotiveScraper(),
            WeWorkRemotelyScraper(),
            WellfoundScraper(),
            YCJobsScraper()
        ]

    def run_cycle(self):
        """Executes one full automation cycle."""
        logger.info("=" * 50)
        logger.info("Starting Job Automation Cycle")
        logger.info("=" * 50)
        
        try:
            # 1. Scrape all sources
            raw_jobs = self._scrape_all()
            if not raw_jobs:
                logger.warning("No jobs found in this cycle. Skipping processing.")
                return

            # 2. Filter and Normalize
            logger.info(f"Filtering {len(raw_jobs)} raw listings...")
            filtered_df = job_filter.filter_jobs(raw_jobs)
            if filtered_df.empty:
                logger.info("No relevant jobs found after filtering.")
                return

            # 3. Deduplicate and Score
            logger.info("Applying scoring and local deduplication...")
            processed_df = job_scorer.process(filtered_df)
            
            # 4. Notify via Telegram (Top 5 High-Priority)
            logger.info("Sending notifications for top opportunities...")
            notifier.send_notification(processed_df)

            # 5. Sync to Google Sheets (Cloud deduplication happens here)
            logger.info("Syncing with Google Sheets Tracker...")
            tracker.sync_jobs(processed_df)

            logger.info("Cycle completed successfully.")
            
        except Exception as e:
            logger.critical(f"FATAL: Critical error in automation cycle: {e}", exc_info=True)

    def _scrape_all(self) -> List[dict]:
        """Runs all scrapers and collects results."""
        all_jobs = []
        for scraper in self.scrapers:
            try:
                logger.info(f"Running scraper: {scraper.name}")
                jobs = scraper.run()
                all_jobs.extend(jobs)
                logger.info(f"Successfully fetched {len(jobs)} jobs from {scraper.name}")
            except Exception as e:
                logger.error(f"Error running scraper {scraper.name}: {e}")
                # Continue with other scrapers if one fails
                continue
        return all_jobs

def main():
    """Main entry point."""
    orchestrator = JobAutomationOrchestrator()
    
    # Run once immediately
    orchestrator.run_cycle()

    # Option 1: Daily Scheduling (Default: 10:00 AM)
    # You can change this to match your preference
    scheduled_time = "10:00"
    logger.info(f"Scheduling daily automation at {scheduled_time}")
    schedule.every().day.at(scheduled_time).do(orchestrator.run_cycle)

    # Option 2: Interval Scheduling (Legacy fallback)
    # interval = settings.SCRAPE_INTERVAL_MINUTES
    # logger.info(f"Scheduling automation every {interval} minutes.")
    # schedule.every(interval).minutes.do(orchestrator.run_cycle)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Automation stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
