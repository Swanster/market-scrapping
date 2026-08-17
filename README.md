# Market Analysis & Scraping Platform

Aplikasi analisis tren dan demand pasar e-commerce (TikTok Shop & Shopee) dengan visualisasi dashboard, filter waktu (real-time, mingguan, bulanan, tahunan), dan kemampuan export ke Excel serta PDF.

---

## 📁 Struktur Proyek

```text
market-scrapping/
├── PRD.md                  # Dokumen kebutuhan produk
├── .gitignore              # Global git ignore
├── backend/                # Backend API (FastAPI)
│   ├── app/
│   │   ├── main.py         # Entry point FastAPI & endpoint export/scrape
│   │   ├── models.py       # Pydantic schema (ProductItem, ScrapeRequest, dll)
│   │   ├── scrapers/       # Engine scraping modular (Base, Shopee, TikTok)
│   │   └── services/       # Layanan export PDF & Excel
│   ├── tests/              # Test suite pytest
│   ├── requirements.txt    # Dependensi Python
│   └── venv/               # Virtual environment Python
└── frontend/               # Web Dashboard (Next.js 16 + Tailwind CSS)
    ├── app/                # App router Next.js & halaman Dashboard
    ├── types/              # TypeScript interface & type definitions
    └── package.json        # Dependensi frontend & script pnpm
```

---

## 🚀 Cara Menjalankan

### 1. Backend (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Jalankan server development
uvicorn app.main:app --reload --port 8000
```

- API Docs / Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 2. Frontend (Next.js)

```bash
cd frontend
pnpm install
pnpm dev
```

- Web Dashboard: `http://localhost:3000`

---

## 🧪 Testing

### Backend Testing (Pytest)
```bash
PYTHONPATH=backend backend/venv/bin/pytest backend/tests
```

### Frontend Build Verification
```bash
cd frontend && pnpm run build
```
