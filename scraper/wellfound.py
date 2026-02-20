import time
import random
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class WellfoundScraper(BaseScraper):
    def __init__(self):
        super().__init__("Wellfound")
        # Direct URL to remote internship jobs
        self.base_url = "https://www.wellfound.com/role/l/internship/remote"

    def scrape(self, page):
        logger.info(f"Navigating to {self.base_url}")
        
        # Adding random user-agent and extra headers to avoid bot detection
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        })
        
        try:
            page.goto(self.base_url, wait_until="domcontentloaded")
            # Wait for content to load, or handle potential login wall/challenge
            time.sleep(random.uniform(3, 5))
            
            # Scroll to trigger lazy loading
            for _ in range(3):
                page.mouse.wheel(0, 800)
                time.sleep(random.uniform(1, 2))

            jobs = []
            # Selector for job cards - noted that Wellfound often changes classes
            # Using a more robust combination of data attributes and structure
            job_elements = page.query_selector_all('[data-test="StartupResult"]')
            
            if not job_elements:
                logger.warning("No job elements found on Wellfound. Possible bot block or selector change.")
                # Fallback selector check
                job_elements = page.query_selector_all(".styles_startupCard__")

            for el in job_elements:
                try:
                    # Extracts info from within the card
                    company_el = el.query_selector('[data-test="StartupName"]')
                    company = company_el.inner_text().strip() if company_el else "N/A"
                    
                    # Job listings within a startup card
                    listing_elements = el.query_selector_all('[data-test="JobResult"]')
                    
                    for job_el in listing_elements:
                        role_el = job_el.query_selector('a[data-test="JobTitle"]')
                        role = role_el.inner_text().strip() if role_el else "N/A"
                        
                        apply_path = role_el.get_attribute("href") if role_el else ""
                        apply_link = f"https://wellfound.com{apply_path}" if apply_path else "N/A"
                        
                        # Location and Remote status
                        info_els = job_el.query_selector_all(".styles_jobInfo__ span")
                        location = "Remote"
                        remote_status = "Remote"
                        if info_els:
                            location = info_els[0].inner_text().strip()
                        
                        jobs.append({
                            "Company": company,
                            "Role": role,
                            "Location": location,
                            "Remote/On-site": remote_status,
                            "Apply Link": apply_link,
                            "Source": "Wellfound"
                        })
                except Exception as e:
                    logger.error(f"Error parsing a Wellfound company card: {e}")
                    continue

            return jobs
        except Exception as e:
            logger.error(f"Critical error on Wellfound: {e}")
            return []
