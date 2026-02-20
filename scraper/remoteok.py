from playwright.async_api import async_playwright
import asyncio
import random
from scraper.base_scraper import BaseScraper
from utils.logger import logger

class RemoteOKScraper(BaseScraper):
    def __init__(self):
        super().__init__("RemoteOK")
        self.url = "https://remoteok.com/"

    async def scrape(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            
            logger.info(f"Navigating to {self.url}")
            await page.goto(self.url, wait_until="networkidle")
            
            # Handle infinite scroll
            for _ in range(3):
                await page.mouse.wheel(0, 2000)
                await asyncio.sleep(random.uniform(1, 3))

            jobs = []
            rows = await page.query_selector_all("tr.job")
            
            for row in rows:
                try:
                    role = await row.query_selector("h2[itemprop='title']")
                    company = await row.query_selector("h3[itemprop='name']")
                    location = await row.query_selector("div.location")
                    apply_link = await row.get_attribute("data-href")
                    tags_elements = await row.query_selector_all("td.tags .tag h3")
                    date_element = await row.query_selector("time")

                    tags = [await tag.inner_text() for tag in tags_elements]
                    
                    job_data = {
                        "company": (await company.inner_text()).strip() if company else "N/A",
                        "role": (await role.inner_text()).strip() if role else "N/A",
                        "location": (await location.inner_text()).strip() if location else "Remote",
                        "tags": tags,
                        "apply_link": f"https://remoteok.com{apply_link}" if apply_link else self.url,
                        "date": await date_element.get_attribute("datetime") if date_element else "N/A"
                    }
                    jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Failed to parse a row in RemoteOK: {e}")

            await browser.close()
            logger.info(f"Extracted {len(jobs)} jobs from RemoteOK")
            return jobs

    def run(self):
        return asyncio.run(self.scrape())

if __name__ == "__main__":
    scraper = RemoteOKScraper()
    results = scraper.run()
    print(results[:2])  # Print first two results for verification
