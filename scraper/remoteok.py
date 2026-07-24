from scraper.base_scraper import BaseScraper
from utils.logger import logger


class RemoteOKScraper(BaseScraper):
    """Pulls jobs from RemoteOK's public JSON API (https://remoteok.com/api)."""

    def __init__(self):
        super().__init__("RemoteOK")
        self.api_url = "https://remoteok.com/api"

    def scrape(self):
        logger.info(f"Fetching {self.api_url}")
        data = self.fetch(self.api_url).json()

        jobs = []
        for item in data:
            # The first element is a legal/metadata object with no job id.
            if not isinstance(item, dict) or not item.get("id"):
                continue

            tags = item.get("tags") or []
            jobs.append({
                "Company": item.get("company", "N/A"),
                "Role": item.get("position", "N/A"),
                "Location": item.get("location") or "Remote",
                "Tags": ", ".join(tags),
                "Apply Link": item.get("url", "N/A"),
                "Date": item.get("date", ""),
                "Description": self.strip_html(item.get("description", "")),
                "Source": "RemoteOK",
            })

        logger.info(f"RemoteOK returned {len(jobs)} listings.")
        return jobs
