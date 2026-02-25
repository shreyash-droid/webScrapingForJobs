from scraper.base_scraper import BaseScraper
from utils.logger import logger
import time

class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__("Indeed")
        # Search for UI, UX, Product, Frontend Internship roles
        self.search_url = "https://www.indeed.com/jobs?q=UI+UX+Product+Frontend+internship&l=Remote&fromage=7"

    def scrape(self, page):
        """Implement the Indeed-specific scraping logic."""
        jobs = []
        
        try:
            # Add human-like behavior
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            })
            
            logger.info(f"Navigating to {self.search_url}")
            # Use a longer timeout for Indeed
            page.goto(self.search_url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for job cards to appear
            try:
                page.wait_for_selector(".cardOutline", timeout=15000)
            except Exception:
                logger.warning("Job cards not found on Indeed. Site might be blocking or selectors changed.")
                return []

            # Extract job elements
            job_cards = page.query_selector_all(".cardOutline")
            
            for card in job_cards:
                try:
                    # Selectors based on Indeed's common structure
                    title_el = card.query_selector("h2.jobTitle span[title]")
                    company_el = card.query_selector("[data-testid='company-name']")
                    location_el = card.query_selector("[data-testid='text-location']")
                    link_el = card.query_selector("h2.jobTitle a")
                    
                    if title_el and link_el:
                        title = title_el.inner_text().strip()
                        company = company_el.inner_text().strip() if company_el else "N/A"
                        location = location_el.inner_text().strip() if location_el else "Remote"
                        
                        # Indeed links are often relative
                        link = link_el.get_attribute("href")
                        if link and link.startswith("/"):
                            link = "https://www.indeed.com" + link
                        
                        jobs.append({
                            "Role": title,
                            "Company": company,
                            "Location": location,
                            "Apply Link": link,
                            "Source": self.name,
                            "Tags": "Indeed, Internship"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing job card on Indeed: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error during scraping with {self.name}: {e}")
                
        return jobs
