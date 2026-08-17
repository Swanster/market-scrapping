from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.models import ScrapeRequest, ScrapeResponse, TimeRange, Platform, ProductItem
from app.services.exporter import export_to_excel, export_to_pdf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("market-scrapping")

app = FastAPI(
    title="Market Scraping API",
    description="Backend API for Market Analysis & Demand Tracking (TikTok Shop & Shopee)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock cache/in-memory store for recent search results
LAST_RESULTS = {}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "market-scrapping-api"}

@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_products(payload: ScrapeRequest):
    logger.info(f"Received scrape request: {payload.keyword} [{payload.time_range.value}]")
    
    # Mock / Prototype Response Data for Initial Scaffolding Verification
    mock_items = [
        ProductItem(
            rank=i + 1,
            name=f"Contoh Produk {payload.keyword.capitalize()} Unggulan #{i+1}",
            price=15000.0 * (i + 1),
            price_formatted=f"Rp {(15000 * (i + 1)):,.0f}".replace(",", "."),
            sales_volume=10000 // (i + 1),
            sales_volume_formatted=f"{10000 // (i + 1):,} terjual".replace(",", "."),
            rating=4.8 - (i * 0.05),
            reviews_count=1200 // (i + 1),
            shop_name=f"Official Store {payload.keyword.capitalize()} {i+1}",
            product_url="https://shopee.co.id",
            platform="shopee" if i % 2 == 0 else "tiktok",
            image_url="https://via.placeholder.com/150"
        )
        for i in range(payload.limit)
    ]
    
    response_data = ScrapeResponse(
        query=payload.keyword,
        time_range=payload.time_range,
        platform=payload.platform,
        total_found=len(mock_items),
        data=mock_items
    )
    
    cache_key = f"{payload.keyword}_{payload.time_range.value}_{payload.platform.value}"
    LAST_RESULTS[cache_key] = response_data
    
    return response_data

@app.get("/api/export/excel")
async def export_excel(
    keyword: str = Query(..., description="Target keyword"),
    time_range: TimeRange = Query(TimeRange.MONTHLY),
    platform: Platform = Query(Platform.ALL)
):
    cache_key = f"{keyword}_{time_range.value}_{platform.value}"
    result = LAST_RESULTS.get(cache_key)
    if not result:
        # Generate on the fly if not cached
        scrape_res = await scrape_products(ScrapeRequest(keyword=keyword, time_range=time_range, platform=platform, limit=10))
        result = scrape_res
        
    excel_bytes = export_to_excel(result.data, keyword, time_range.value)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=market_analysis_{keyword}.xlsx"}
    )

@app.get("/api/export/pdf")
async def export_pdf(
    keyword: str = Query(..., description="Target keyword"),
    time_range: TimeRange = Query(TimeRange.MONTHLY),
    platform: Platform = Query(Platform.ALL)
):
    cache_key = f"{keyword}_{time_range.value}_{platform.value}"
    result = LAST_RESULTS.get(cache_key)
    if not result:
        scrape_res = await scrape_products(ScrapeRequest(keyword=keyword, time_range=time_range, platform=platform, limit=10))
        result = scrape_res
        
    pdf_bytes = export_to_pdf(result.data, keyword, time_range.value)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=market_analysis_{keyword}.pdf"}
    )
