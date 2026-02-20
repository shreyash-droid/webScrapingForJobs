import time
import random
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class YCJobsScraper(BaseScraper):
    def __init__(self):
        super().__init__("YC Jobs")
        self.base_url = "https://www.workatastartup.com/jobs?job_type=internship"

    def scrape(self, page):
        logger.info(f"Navigating to {self.base_url}")
        
        # YC uses dynamic content heavily
        try:
            page.goto(self.base_url, wait_until="networkidle")
            time.sleep(random.uniform(2, 4))
            
            # Scroll to load more jobs
            for _ in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(random.uniform(1, 2))

            jobs = []
            # Selector for job items
            job_elements = page.query_selector_all(".job-listing")
            
            if not job_elements:
                # Fallback for updated UI
                job_elements = page.query_selector_all(".styles_jobCard__")

            for el in job_elements:
                try:
                    company_el = el.query_selector(".company-name")
                    company = company_el.inner_text().strip() if company_el else "N/A"
                    
                    role_el = el.query_selector(".job-name a")
                    role = role_el.inner_text().strip() if role_el else "N/A"
                    
                    apply_path = role_el.get_attribute("href") if role_el else ""
                    apply_link = apply_path if apply_path.startswith("http") else f"https://www.workatastartup.com{apply_path}"
                    
                    location_el = el.query_selector(".job-location")
                    location_text = location_el.inner_text().strip() if location_el else "Remote"
                    
                    is_remote = "Remote" if "Remote" in location_text else "On-site/Hybrid"

                    jobs.append({
                        "Company": company,
                        "Role": role,
                        "Location": location_text,
                        "Remote/On-site": is_remote,
                        "Apply Link": apply_link,
                        "Source": "YC Jobs"
                    })
                except Exception as e:
                    logger.error(f"Error parsing a YC job listing: {e}")
                    continue

            return jobs
        except Exception as e:
            logger.error(f"Critical error on YC Jobs: {e}")
            return []
