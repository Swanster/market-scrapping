import asyncio
from typing import List
from app.models import ProductItem, TimeRange, Platform
from app.scrapers.shopee import ShopeeScraper
from app.scrapers.tiktok import TikTokScraper
import logging

logger = logging.getLogger(__name__)

class ScraperPipeline:
    def __init__(self):
        self.shopee = ShopeeScraper()
        self.tiktok = TikTokScraper()

    async def run(self, keyword: str, time_range: TimeRange, platform: Platform = Platform.ALL, limit: int = 10) -> List[ProductItem]:
        logger.info(f"Pipeline running for keyword='{keyword}', range='{time_range.value}', platform='{platform.value}', limit={limit}")
        
        all_items: List[ProductItem] = []
        
        if platform == Platform.SHOPEE:
            all_items = await self.shopee.scrape(keyword, time_range, limit=limit)
        elif platform == Platform.TIKTOK:
            all_items = await self.tiktok.scrape(keyword, time_range, limit=limit)
        else:
            # Platform.ALL -> Scrape both in parallel, then merge & rank
            target_per_source = max(5, limit // 2 + 2)
            results = await asyncio.gather(
                self.shopee.scrape(keyword, time_range, limit=target_per_source),
                self.tiktok.scrape(keyword, time_range, limit=target_per_source),
                return_exceptions=True
            )
            
            shopee_res, tiktok_res = results[0], results[1]
            if isinstance(shopee_res, list):
                all_items.extend(shopee_res)
            else:
                logger.error(f"Shopee scrape failed: {shopee_res}")
                
            if isinstance(tiktok_res, list):
                all_items.extend(tiktok_res)
            else:
                logger.error(f"TikTok scrape failed: {tiktok_res}")

        # Sort descending by sales volume
        all_items.sort(key=lambda p: p.sales_volume, reverse=True)
        
        # Take top N and re-rank
        final_items = all_items[:limit]
        for idx, item in enumerate(final_items):
            item.rank = idx + 1
            
        return final_items
