from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class TimeRange(str, Enum):
    REALTIME = "realtime"  # 24h
    WEEKLY = "weekly"      # 7d
    MONTHLY = "monthly"    # 30d
    YEARLY = "yearly"      # 365d

class Platform(str, Enum):
    ALL = "all"
    SHOPEE = "shopee"
    TIKTOK = "tiktok"

class ProductItem(BaseModel):
    rank: int
    name: str
    price: float
    price_formatted: str
    sales_volume: int
    sales_volume_formatted: str
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    reviews_count: int = 0
    shop_name: str
    product_url: str
    platform: str
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)

class ScrapeRequest(BaseModel):
    keyword: str
    time_range: TimeRange = TimeRange.MONTHLY
    platform: Platform = Platform.ALL
    limit: int = Field(default=10, ge=1, le=50)

class ScrapeResponse(BaseModel):
    query: str
    time_range: TimeRange
    platform: Platform
    total_found: int
    data: List[ProductItem]
    scraped_at: datetime = Field(default_factory=utc_now)
