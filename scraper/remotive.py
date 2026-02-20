from playwright.async_api import async_playwright
import asyncio
import random
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class RemotiveScraper(BaseScraper):
    def __init__(self):
        super().__init__("Remotive")
        self.url = "https://remotive.com/remote-jobs"

    async def scrape(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            
            logger.info(f"Navigating to {self.url}")
            await page.goto(self.url, wait_until="networkidle")
            
            # Wait for job items to load
            await page.wait_for_selector(".remotive-job-item", timeout=10000)

            jobs = []
            items = await page.query_selector_all(".remotive-job-item")
            
            for item in items:
                try:
                    role = await item.query_selector(".remotive-job-item__title")
                    company = await item.query_selector(".remotive-job-item__company")
                    location = await item.query_selector(".remotive-job-item__location")
                    tags_elements = await item.query_selector_all(".remotive-job-item__tag")
                    date_element = await item.query_selector(".remotive-job-item__publish-date")
                    
                    # Apply link is usually the href of the item container or title
                    link_element = await item.query_selector("a")
                    apply_link = await link_element.get_attribute("href") if link_element else None

                    tags = [await tag.inner_text() for tag in tags_elements]
                    
                    job_data = {
                        "company": (await company.inner_text()).strip() if company else "N/A",
                        "role": (await role.inner_text()).strip() if role else "N/A",
                        "location": (await location.inner_text()).strip() if location else "Remote",
                        "tags": tags,
                        "apply_link": f"https://remotive.com{apply_link}" if apply_link and apply_link.startswith("/") else apply_link,
                        "date": (await date_element.inner_text()).strip() if date_element else "N/A"
                    }
                    jobs.append(job_data)
                    
                    # Random delay to be polite
                    if random.random() > 0.8:
                        await asyncio.sleep(0.1)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse a row in Remotive: {e}")

            await browser.close()
            logger.info(f"Extracted {len(jobs)} jobs from Remotive")
            return jobs

    def run(self):
        return asyncio.run(self.scrape())

if __name__ == "__main__":
    scraper = RemotiveScraper()
    results = scraper.run()
    print(results[:2])
