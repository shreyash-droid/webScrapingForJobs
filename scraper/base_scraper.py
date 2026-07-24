import re
from abc import ABC, abstractmethod

import requests

from utils.logger import logger


class BaseScraper(ABC):
    """
    Base class for API / RSS based job scrapers.

    Sources are fetched over plain HTTP (no headless browser), which is far more
    reliable and faster than DOM scraping and gives us real job descriptions to
    filter and score against.
    """

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 CareerBot/1.0"
        ),
        "Accept": "application/json, text/xml, text/html, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, name):
        self.name = name

    def run(self):
        """Runs the scraper, isolating failures so one bad source can't crash the cycle."""
        logger.info(f"Starting scraper: {self.name}")
        try:
            jobs = self.scrape()
            return jobs or []
        except requests.RequestException as e:
            logger.error(f"Network error in {self.name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error during scraping with {self.name}: {e}")
            return []

    def fetch(self, url, timeout=30, **kwargs):
        """GET a URL with sane defaults and raise on HTTP errors."""
        resp = requests.get(url, headers=self.HEADERS, timeout=timeout, **kwargs)
        resp.raise_for_status()
        return resp

    @staticmethod
    def strip_html(text):
        """Turns an HTML description snippet into plain text for matching/scoring."""
        if not text:
            return ""
        text = re.sub(r"<[^>]+>", " ", text)          # drop tags
        text = re.sub(r"&[a-zA-Z#0-9]+;", " ", text)   # drop HTML entities
        return re.sub(r"\s+", " ", text).strip()

    @abstractmethod
    def scrape(self):
        """Fetch and return a list of job dicts. Implement per source."""
        raise NotImplementedError
