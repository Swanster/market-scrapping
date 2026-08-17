# Product Requirement Document: Market Analysis Application

## 1. Overview
A web-based market analysis application that scrapes product data from TikTok Shop and Shopee, ranks products by purchase frequency, and provides filtering by time range (real-time, weekly, monthly, yearly). Results displayed on a dashboard with export capabilities to PDF and Excel, including product links.

## 2. Target Users
- Market analysts
- Business owners researching product demand
- Entrepreneurs sourcing trending products
- Researchers tracking e-commerce trends

## 3. Core Features

### 3.1 Product Input
- User enters product type/keyword (e.g., "kebutuhan sehari hari", "minyak", "sabun")
- Auto-suggest or validation for supported categories

### 3.2 Data Scraping
- **Sources**: TikTok Shop, Shopee (configurable per deployment)
- **Data points per product**:
  - Product name
  - Price
  - Monthly sales volume / purchase count
  - Average rating
  - Number of reviews
  - Shop name
  - Product link (URL)
- **Time filtering options**:
  - Real-time (last 24 hours)
  - Weekly (last 7 days)
  - Monthly (last 30 days)
  - Yearly (last 365 days)
- Sorting: Descending by purchase frequency (most bought first)
- Output: Top 10 products per query

### 3.3 Dashboard Display
- Card/list view of top 10 products
- Each card shows:
  - Product rank
  - Product name (truncated if long)
  - Price
  - Sales volume / purchase count
  - Rating (stars)
  - Shop name
  - Product link (clickable, opens in new tab)
- Time range selector UI (toggle buttons or dropdown)
- Real-time data refresh indicator

### 3.4 Export Functionality
- **PDF export**:
  - formatted report with title, date range, top 10 products table
  - Includes product images (thumbnails) if available
  - Downloadable via button
- **Excel export**:
  - Columns: Rank, Product Name, Price, Sales Volume, Rating, Reviews Count, Shop Name, Product Link
  - Downloadable via button
- Both exports include timestamp and query parameters

### 3.5 Admin / Configuration (optional)
- Platform selection (TikTok, Shopee, both)
- Scraping frequency settings
- Proxy/configuration for data collection

## 4. User Flow
1. User opens dashboard
2. User enters product type keyword in input field
3. User selects time range (real-time/weekly/monthly/yearly)
4. System scrapes data from configured platforms
5. System ranks results by purchase frequency, shows top 10
6. User views results on dashboard
7. User clicks export → PDF or Excel download
8. User clicks product link → opens original product page

## 5. Technical Requirements

### 5.1 Frontend
- React or Next.js application
- Responsive design for mobile/web
- State management for search queries and results
- PDF generation library (e.g., jsPDF)
- Excel file generation (e.g., sheet.js, exceljs)

### 5.2 Backend
- Python or Node.js API server
- Scraping engine (Playwright, Selenium, or similar for dynamic content)
- Data processing pipeline (normalize, rank, filter)
- Caching layer for repeated queries
- API endpoints:
  - `POST /api/scrape` — trigger scrape with keyword + time range
  - `GET /api/results` — fetch latest results
  - `GET /api/export/pdf` — generate PDF
  - `GET /api/export/excel` — generate Excel

### 5.3 Data Sources
- **TikTok Shop**: requires handling dynamic loading, anti-bot measures
- **Shopee**: standard e-commerce scraping with proper selectors
- Rate limiting and respect for platform TOS
- Proxy rotation if needed for high-volume scraping

### 5.4 Database (optional but recommended)
- Store query history
- Store scraping results with timestamps
- Enable trend analysis over time

## 6. UI/UX Guidelines
- Clean, minimal interface
- Indonesian language support (per user preference)
- Clear indication of data freshness
- Loading states during scraping
- Error handling for no results or platform issues
- Accessible color contrast

## 7. Non-Functional Requirements
- **Performance**: Scrape + rank top 10 within 30-60 seconds
- **Reliability**: Handle temporary platform unavailability gracefully
- **Security**: No credential storage; sanitize all user inputs
- **Scalability**: Support multiple concurrent users with queued scraping
- **Maintainability**: Modular scraping code, easy to add new platforms

## 8. Dependencies & External Services
- Web scraping libraries (Playwright/Selenium)
- PDF generation library
- Excel file generation library
- Optional: proxy services for IP rotation
- Database (PostgreSQL/MySQL) for result history

## 9. Roadmap / Milestones
1. **Week 1**: PRD approval, project setup, scaffolding
2. **Week 2**: Scraping engine for Shopee, basic data extraction
3. **Week 3**: TikTok Shop scraping, data normalization
4. **Week 4**: Dashboard UI, time filter implementation
5. **Week 5**: Export functionality (PDF + Excel)
6. **Week 6**: Testing, bug fixes, documentation
7. **Week 7**: Deployment and user acceptance testing

## 10. Success Metrics
- Accuracy of top 10 ranking by purchase frequency
- Scraping success rate per platform
- User satisfaction with dashboard UX
- Export file correctness (data matches dashboard)
- System uptime and reliability

---
*PRD created for market analysis application — user enters product type, gets top 10 most bought products sorted by frequency, with time range filtering, web dashboard, and PDF/Excel export with product links.*