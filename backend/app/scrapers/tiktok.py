from typing import List
from app.scrapers.base import BaseScraper
from app.models import ProductItem, TimeRange
import logging

logger = logging.getLogger(__name__)

class TikTokScraper(BaseScraper):
    @property
    def platform_name(self) -> str:
        return "tiktok"

    async def scrape(self, keyword: str, time_range: TimeRange, limit: int = 10) -> List[ProductItem]:
        # Implementasi engine scraper TikTok Shop
        logger.info(f"Scraping TikTok for keyword='{keyword}' range='{time_range.value}'")
        return []
