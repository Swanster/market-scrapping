from abc import ABC, abstractmethod
from typing import List
from app.models import ProductItem, TimeRange

class BaseScraper(ABC):
    @property
    @abstractmethod
    def platform_name(self) -> str:
        pass

    @abstractmethod
    async def scrape(self, keyword: str, time_range: TimeRange, limit: int = 10) -> List[ProductItem]:
        """Scrapes products from the platform according to keyword and time range."""
        pass
