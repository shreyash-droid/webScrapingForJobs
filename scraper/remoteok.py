import time
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class RemoteOKScraper(BaseScraper):
    def __init__(self):
        super().__init__("RemoteOK")
        self.base_url = "https://remoteok.com/remote-internship-jobs"

    def scrape(self, page):
        logger.info(f"Navigating to {self.base_url}")
        page.goto(self.base_url, wait_until="networkidle")
        
        # Human-like delay
        time.sleep(2)
        
        # RemoteOK often has a popup or requires scrolling
        page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
        time.sleep(1)

        jobs = []
        # RemoteOK jobs are in rows with class 'job'
        job_elements = page.query_selector_all("tr.job")
        
        for el in job_elements:
            try:
                company = el.get_attribute("data-company")
                role = el.query_selector("h2").inner_text().strip() if el.query_selector("h2") else "N/A"
                
                # Tags are usually in a div with class 'tags'
                tags = [tag.inner_text().strip() for tag in el.query_selector_all(".tag h3")]
                
                # Location is often in a div with class 'location'
                location_el = el.query_selector(".location")
                location = location_el.inner_text().strip() if location_el else "Remote"
                
                # Apply link
                apply_path = el.get_attribute("data-href")
                apply_link = f"https://remoteok.com{apply_path}" if apply_path else "N/A"
                
                # Date
                date_el = el.query_selector(".time time")
                date = date_el.get_attribute("datetime") if date_el else "N/A"

                jobs.append({
                    "Company": company,
                    "Role": role,
                    "Location": location,
                    "Tags": ", ".join(tags),
                    "Apply Link": apply_link,
                    "Date": date,
                    "Source": "RemoteOK"
                })
            except Exception as e:
                logger.error(f"Error parsing a job row in RemoteOK: {e}")
                continue

        return jobs
