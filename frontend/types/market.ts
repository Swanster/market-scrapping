export interface ProductItem {
  rank: number;
  name: string;
  price: number;
  price_formatted: string;
  sales_volume: number;
  sales_volume_formatted: string;
  rating: number;
  reviews_count: number;
  shop_name: string;
  product_url: string;
  platform: 'shopee' | 'tiktok' | string;
  image_url?: string;
  created_at: string;
}

export type TimeRange = 'realtime' | 'weekly' | 'monthly' | 'yearly';
export type Platform = 'all' | 'shopee' | 'tiktok';

export interface ScrapeResponse {
  query: string;
  time_range: TimeRange;
  platform: Platform;
  total_found: number;
  data: ProductItem[];
  scraped_at: string;
}
