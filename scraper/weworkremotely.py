import xml.etree.ElementTree as ET

from scraper.base_scraper import BaseScraper
from utils.logger import logger
from config.settings import settings


class WeWorkRemotelyScraper(BaseScraper):
    """Pulls jobs from We Work Remotely category RSS feeds (no HTML scraping needed)."""

    def __init__(self):
        super().__init__("WeWorkRemotely")
        self.feed_base = "https://weworkremotely.com/categories"

    def scrape(self):
        jobs = []
        for slug in settings.WWR_FEEDS:
            url = f"{self.feed_base}/{slug}.rss"
            logger.info(f"Fetching {url}")
            try:
                content = self.fetch(url).content
                root = ET.fromstring(content)
            except Exception as e:
                logger.error(f"WWR feed '{slug}' failed: {e}")
                continue

            for item in root.iter("item"):
                title_raw = (item.findtext("title") or "").strip()
                # WWR titles are formatted "Company: Role Title".
                if ":" in title_raw:
                    company, role = [p.strip() for p in title_raw.split(":", 1)]
                else:
                    company, role = "N/A", title_raw

                jobs.append({
                    "Company": company or "N/A",
                    "Role": role or "N/A",
                    "Location": (item.findtext("region") or "Remote").strip(),
                    "Tags": (item.findtext("category") or "").strip(),
                    "Apply Link": (item.findtext("link") or "N/A").strip(),
                    "Date": (item.findtext("pubDate") or "").strip(),
                    "Description": self.strip_html(item.findtext("description") or ""),
                    "Source": "WeWorkRemotely",
                })

        logger.info(f"WeWorkRemotely returned {len(jobs)} listings.")
        return jobs
