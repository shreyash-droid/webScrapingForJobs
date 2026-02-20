import time
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class WeWorkRemotelyScraper(BaseScraper):
    def __init__(self):
        super().__init__("WeWorkRemotely")
        self.base_url = "https://weworkremotely.com/remote-jobs/search?term=internship"

    def scrape(self, page):
        logger.info(f"Navigating to {self.base_url}")
        page.goto(self.base_url, wait_until="networkidle")
        
        time.sleep(2)
        
        jobs = []
        # WWR jobs are in list items <li> within a section
        job_elements = page.query_selector_all("section.jobs article ul li:not(.view-all)")
        
        for el in job_elements:
            try:
                # Some <li> might be headers or dividers
                if not el.query_selector(".title"):
                    continue
                    
                role_el = el.query_selector(".title")
                role = role_el.inner_text().strip() if role_el else "N/A"
                
                company_el = el.query_selector(".company")
                company = company_el.inner_text().strip() if company_el else "N/A"
                
                region_el = el.query_selector(".region")
                location = region_el.inner_text().strip() if region_el else "Remote"
                
                # Apply link
                link_els = el.query_selector_all("a")
                # Usually there are two links, one for the whole item
                apply_link = "N/A"
                for link in link_els:
                    href = link.get_attribute("href")
                    if href and "/remote-jobs/" in href:
                        apply_link = f"https://weworkremotely.com{href}"
                        break
                
                # Date
                date_el = el.query_selector("time")
                date = date_el.get_attribute("datetime") if date_el else "N/A"

                jobs.append({
                    "Company": company,
                    "Role": role,
                    "Location": location,
                    "Tags": "Internship", # Fixed tag based on search
                    "Apply Link": apply_link,
                    "Date": date,
                    "Source": "WeWorkRemotely"
                })
            except Exception as e:
                logger.error(f"Error parsing a job item in WeWorkRemotely: {e}")
                continue

        return jobs
