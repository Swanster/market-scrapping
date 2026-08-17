from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.models import ScrapeRequest, ScrapeResponse, TimeRange, Platform, ProductItem
from app.scrapers.pipeline import ScraperPipeline
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

pipeline = ScraperPipeline()

# In-memory cache for recent search queries
CACHE_STORE = {}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "market-scrapping-api"}

@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_products(payload: ScrapeRequest):
    logger.info(f"Received scrape request: {payload.keyword} [{payload.time_range.value}] [{payload.platform.value}]")
    
    cache_key = f"{payload.keyword.lower().strip()}_{payload.time_range.value}_{payload.platform.value}_{payload.limit}"
    if cache_key in CACHE_STORE:
        logger.info(f"Returning cached response for key: {cache_key}")
        return CACHE_STORE[cache_key]
    
    try:
        items = await pipeline.run(
            keyword=payload.keyword,
            time_range=payload.time_range,
            platform=payload.platform,
            limit=payload.limit
        )
    except Exception as e:
        logger.error(f"Scraping error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gagal melakukan scraping pasar: {str(e)}")

    response_data = ScrapeResponse(
        query=payload.keyword,
        time_range=payload.time_range,
        platform=payload.platform,
        total_found=len(items),
        data=items
    )
    
    CACHE_STORE[cache_key] = response_data
    return response_data

@app.get("/api/export/excel")
async def export_excel(
    keyword: str = Query(..., description="Target keyword"),
    time_range: TimeRange = Query(TimeRange.MONTHLY),
    platform: Platform = Query(Platform.ALL)
):
    cache_key = f"{keyword.lower().strip()}_{time_range.value}_{platform.value}_10"
    result = CACHE_STORE.get(cache_key)
    if not result:
        items = await pipeline.run(keyword=keyword, time_range=time_range, platform=platform, limit=10)
        result = ScrapeResponse(
            query=keyword,
            time_range=time_range,
            platform=platform,
            total_found=len(items),
            data=items
        )
        CACHE_STORE[cache_key] = result
        
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
    cache_key = f"{keyword.lower().strip()}_{time_range.value}_{platform.value}_10"
    result = CACHE_STORE.get(cache_key)
    if not result:
        items = await pipeline.run(keyword=keyword, time_range=time_range, platform=platform, limit=10)
        result = ScrapeResponse(
            query=keyword,
            time_range=time_range,
            platform=platform,
            total_found=len(items),
            data=items
        )
        CACHE_STORE[cache_key] = result
        
    pdf_bytes = export_to_pdf(result.data, keyword, time_range.value)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=market_analysis_{keyword}.pdf"}
    )
