from abc import ABC, abstractmethod
from utils.logger import logger

class BaseScraper(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    async def scrape(self):
        """Implement the scraping logic here"""
        pass

    def run(self):
        logger.info(f"Starting scraper: {self.name}")
        try:
            # In a real scenario, this would involve playwright async loops
            pass
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
