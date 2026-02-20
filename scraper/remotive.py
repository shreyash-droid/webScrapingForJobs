import time
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class RemotiveScraper(BaseScraper):
    def __init__(self):
        super().__init__("Remotive")
        self.base_url = "https://remotive.com/remote-jobs/internship"

    def scrape(self, page):
        logger.info(f"Navigating to {self.base_url}")
        page.goto(self.base_url, wait_until="networkidle")
        
        time.sleep(2)
        
        jobs = []
        # Remotive jobs are often in a list with specific classes
        job_elements = page.query_selector_all(".job-list-item")
        
        for el in job_elements:
            try:
                role_el = el.query_selector(".job-tile-title")
                role = role_el.inner_text().strip() if role_el else "N/A"
                
                company_el = el.query_selector(".job-tile-info span:first-child")
                company = company_el.inner_text().strip() if company_el else "N/A"
                
                location_el = el.query_selector(".job-tile-location")
                location = location_el.inner_text().strip() if location_el else "Remote"
                
                # Tags
                tags = [tag.inner_text().strip() for tag in el.query_selector_all(".remotive-tag")]
                
                # Apply link - usually the parent <a> or a specific link
                link_el = el.query_selector("a")
                apply_link = f"https://remotive.com{link_el.get_attribute('href')}" if link_el else "N/A"
                
                # Date
                date_el = el.query_selector(".job-date")
                date = date_el.inner_text().strip() if date_el else "N/A"

                jobs.append({
                    "Company": company,
                    "Role": role,
                    "Location": location,
                    "Tags": ", ".join(tags),
                    "Apply Link": apply_link,
                    "Date": date,
                    "Source": "Remotive"
                })
            except Exception as e:
                logger.error(f"Error parsing a job item in Remotive: {e}")
                continue

        return jobs
