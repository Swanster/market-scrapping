'use client';

import React, { useState } from 'react';
import axios from 'axios';
import { Search, Download, FileSpreadsheet, ExternalLink, RefreshCw, Star, ShoppingBag } from 'lucide-react';
import { ProductItem, ScrapeResponse, TimeRange, Platform } from '@/types/market';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function DashboardPage() {
  const [keyword, setKeyword] = useState('');
  const [timeRange, setTimeRange] = useState<TimeRange>('monthly');
  const [platform, setPlatform] = useState<Platform>('all');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScrapeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyword.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post<ScrapeResponse>(`${API_BASE_URL}/api/scrape`, {
        keyword,
        time_range: timeRange,
        platform,
        limit: 10
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal mengambil data dari server');
    } finally {
      setLoading(false);
    }
  };

  const handleExportExcel = () => {
    if (!keyword) return;
    window.open(`${API_BASE_URL}/api/export/excel?keyword=${encodeURIComponent(keyword)}&time_range=${timeRange}&platform=${platform}`, '_blank');
  };

  const handleExportPDF = () => {
    if (!keyword) return;
    window.open(`${API_BASE_URL}/api/export/pdf?keyword=${encodeURIComponent(keyword)}&time_range=${timeRange}&platform=${platform}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
              <ShoppingBag className="w-8 h-8 text-indigo-500" />
              Market Analysis & Scraping
            </h1>
            <p className="text-slate-400 mt-1">
              Riset demand produk terlaris di TikTok Shop & Shopee secara real-time.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-950/80 text-emerald-400 border border-emerald-800">
              API Status: Ready
            </span>
          </div>
        </header>

        {/* Search & Filter Form */}
        <form onSubmit={handleSearch} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
            <div className="md:col-span-6 relative">
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-2">Kata Kunci / Kategori</label>
              <div className="relative">
                <input
                  type="text"
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  placeholder="Contoh: minyak goreng, skincare, sepatu running..."
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 pl-10 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  required
                />
                <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
              </div>
            </div>

            <div className="md:col-span-3">
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-2">Rentang Waktu</label>
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value as TimeRange)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="realtime">Real-time (24 Jam)</option>
                <option value="weekly">Mingguan (7 Hari)</option>
                <option value="monthly">Bulanan (30 Hari)</option>
                <option value="yearly">Tahunan (365 Hari)</option>
              </select>
            </div>

            <div className="md:col-span-3">
              <label className="block text-xs font-semibold uppercase text-slate-400 mb-2">Platform Target</label>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value as Platform)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="all">Semua Platform</option>
                <option value="shopee">Shopee</option>
                <option value="tiktok">TikTok Shop</option>
              </select>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between pt-2 border-t border-slate-800/60 gap-3">
            <div className="text-xs text-slate-400">
              * Menampilkan top 10 produk dengan frekuensi pembelian tertinggi.
            </div>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all disabled:opacity-50 cursor-pointer"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Menganalisis Pasar...
                </>
              ) : (
                <>
                  <Search className="w-4 h-4" />
                  Analisis Demand
                </>
              )}
            </button>
          </div>
        </form>

        {/* Error Alert */}
        {error && (
          <div className="bg-rose-950/60 border border-rose-800 text-rose-300 p-4 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Results Area */}
        {result && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-4 rounded-xl">
              <div>
                <h2 className="text-lg font-semibold text-white">
                  Hasil Top 10: &quot;{result.query}&quot;
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Filter: {result.time_range} • Ditemukan: {result.total_found} produk
                </p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={handleExportExcel}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-emerald-950 hover:bg-emerald-900 text-emerald-300 border border-emerald-800 text-xs font-medium transition cursor-pointer"
                >
                  <FileSpreadsheet className="w-4 h-4" />
                  Export Excel
                </button>
                <button
                  onClick={handleExportPDF}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-red-950 hover:bg-red-900 text-red-300 border border-red-800 text-xs font-medium transition cursor-pointer"
                >
                  <Download className="w-4 h-4" />
                  Export PDF
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.data.map((item: ProductItem) => (
                <div
                  key={item.rank}
                  className="bg-slate-900 border border-slate-800 hover:border-slate-700 p-5 rounded-xl transition flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-slate-800 text-indigo-400 font-bold text-xs">
                        #{item.rank}
                      </span>
                      <span
                        className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${
                          item.platform === 'shopee'
                            ? 'bg-amber-950/80 text-amber-400 border border-amber-800'
                            : 'bg-cyan-950/80 text-cyan-400 border border-cyan-800'
                        }`}
                      >
                        {item.platform}
                      </span>
                    </div>

                    <h3 className="font-semibold text-slate-100 line-clamp-2 text-sm hover:text-indigo-400 transition mb-2">
                      {item.name}
                    </h3>
                    <p className="text-xs text-slate-400 mb-3">Toko: {item.shop_name}</p>

                    <div className="flex items-baseline justify-between mb-4">
                      <span className="text-lg font-bold text-emerald-400">{item.price_formatted}</span>
                      <span className="text-xs font-medium text-slate-300 bg-slate-800 px-2 py-1 rounded">
                        {item.sales_volume_formatted}
                      </span>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-1 text-amber-400">
                      <Star className="w-3.5 h-3.5 fill-current" />
                      <span>{item.rating}</span>
                      <span className="text-slate-500">({item.reviews_count} ulasan)</span>
                    </div>
                    <a
                      href={item.product_url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-indigo-400 hover:text-indigo-300 font-medium"
                    >
                      Buka Produk <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
