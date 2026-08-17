from typing import List
from app.scrapers.base import BaseScraper
from app.models import ProductItem, TimeRange
import logging

logger = logging.getLogger(__name__)

class ShopeeScraper(BaseScraper):
    @property
    def platform_name(self) -> str:
        return "shopee"

    async def scrape(self, keyword: str, time_range: TimeRange, limit: int = 10) -> List[ProductItem]:
        # Implementasi engine scraper Shopee (API / Playwright headless)
        logger.info(f"Scraping Shopee for keyword='{keyword}' range='{time_range.value}'")
        # Template list; diisi data scraper nyata pada tahap modul scraper
        return []
