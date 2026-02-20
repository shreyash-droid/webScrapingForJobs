import schedule
import time
from config.settings import config
from utils.logger import logger
from scraper.remoteok import RemoteOKScraper
from scraper.remotive import RemotiveScraper
from scraper.weworkremotely import WeWorkRemotelyScraper

def run_all_scrapers():
    logger.info("Initializing scraping cycle...")
    
    scrapers = [
        RemoteOKScraper(),
        RemotiveScraper(),
        WeWorkRemotelyScraper()
    ]
    
    all_jobs = []
    for scraper in scrapers:
        try:
            jobs = scraper.run()
            all_jobs.extend(jobs)
            logger.info(f"Successfully scraped {len(jobs)} jobs from {scraper.name}")
        except Exception as e:
            logger.error(f"Failed to run scraper {scraper.name}: {e}")
            
    logger.info(f"Scraping cycle completed. Total jobs found: {len(all_jobs)}")
    # Here you would typically save all_jobs to a database or Google Sheet

def main():
    logger.info("Starting Job Automation System")
    
    # Schedule the scrapers to run at regular intervals
    schedule.every(config.SCRAPE_INTERVAL).minutes.do(run_all_scrapers)
    
    # Run immediately on start
    run_all_scrapers()

    logger.info(f"System scheduled to run every {config.SCRAPE_INTERVAL} minutes")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("System stopped by user")
    except Exception as e:
        logger.error(f"Critical system failure: {e}")
