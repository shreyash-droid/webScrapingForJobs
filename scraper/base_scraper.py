from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright
from utils.logger import logger

class BaseScraper(ABC):
    def __init__(self, name):
        self.name = name

    def run(self):
        logger.info(f"Starting scraper: {self.name}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                data = self.scrape(page)
                browser.close()
                return data
            except Exception as e:
                logger.error(f"Error during scraping with {self.name}: {e}")
                browser.close()
                return []

    @abstractmethod
    def scrape(self, page):
        """Implement the scraping logic here"""
        pass
