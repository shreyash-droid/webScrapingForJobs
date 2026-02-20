from playwright.async_api import async_playwright
import asyncio
import random
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class WeWorkRemotelyScraper(BaseScraper):
    def __init__(self):
        super().__init__("WeWorkRemotely")
        self.url = "https://weworkremotely.com/"

    async def scrape(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            
            logger.info(f"Navigating to {self.url}")
            await page.goto(self.url, wait_until="networkidle")
            
            jobs = []
            # WWR structure: sections for categories, each containing an <ul> with <li> jobs
            sections = await page.query_selector_all("section.jobs")
            
            for section in sections:
                rows = await section.query_selector_all("li:not(.view-all)")
                for row in rows:
                    try:
                        role = await row.query_selector("span.title")
                        company = await row.query_selector("span.company")
                        location = await row.query_selector("span.region")
                        date_element = await row.query_selector("span.date")
                        
                        # Apply link is in the <a> tag within the row
                        link_element = await row.query_selector("a[href^='/remote-jobs/']")
                        apply_link = await link_element.get_attribute("href") if link_element else None

                        job_data = {
                            "company": (await company.inner_text()).strip() if company else "N/A",
                            "role": (await role.inner_text()).strip() if role else "N/A",
                            "location": (await location.inner_text()).strip() if location else "Remote",
                            "tags": [], # Category is usually the parent section header
                            "apply_link": f"https://weworkremotely.com{apply_link}" if apply_link else self.url,
                            "date": (await date_element.inner_text()).strip() if date_element else "N/A"
                        }
                        jobs.append(job_data)
                    except Exception as e:
                        logger.warning(f"Failed to parse a row in WWR: {e}")

            await browser.close()
            logger.info(f"Extracted {len(jobs)} jobs from WeWorkRemotely")
            return jobs

    def run(self):
        return asyncio.run(self.scrape())

if __name__ == "__main__":
    scraper = WeWorkRemotelyScraper()
    results = scraper.run()
    print(results[:2])
