from scraper.base_scraper import BaseScraper
from utils.logger import logger


class RemotiveScraper(BaseScraper):
    """
    Pulls jobs from Remotive's public JSON API.

    Note: Remotive's free API currently ignores the `category`/`search`/`limit`
    parameters and just returns the latest listings, so we fetch the default feed
    once and let our own title filter select the relevant design/frontend/PM roles.
    """

    def __init__(self):
        super().__init__("Remotive")
        self.api_url = "https://remotive.com/api/remote-jobs"

    def scrape(self):
        logger.info(f"Fetching {self.api_url}")
        payload = self.fetch(self.api_url).json()

        jobs = []
        for item in payload.get("jobs", []):
            tags = item.get("tags") or []
            jobs.append({
                "Company": item.get("company_name", "N/A"),
                "Role": item.get("title", "N/A"),
                "Location": item.get("candidate_required_location") or "Remote",
                "Tags": ", ".join(tags),
                "Apply Link": item.get("url", "N/A"),
                "Date": item.get("publication_date", ""),
                "Description": self.strip_html(item.get("description", "")),
                "Source": "Remotive",
            })

        logger.info(f"Remotive returned {len(jobs)} listings.")
        return jobs
