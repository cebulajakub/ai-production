
export type ShortageSeverity = 'HIGH' | 'MEDIUM' | 'LOW';

export interface InventorySummary {
  total_products_with_shortages: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
}

export interface MaterialShortage {
  sku: string;
  product_name: string;
  total_demand: number;
  quantity_on_hand: number;
  shortage: number;
  severity: ShortageSeverity;
}

export interface DelayedOrder {
  order_id: number;
  customer_name: string;
  status: string;
  expected_delivery_date: string;
}

export interface LowStockProduct {
  product_id: number;
  sku: string;
  product_name: string;
  quantity_on_hand: number;
}

export interface DashboardData {
  summary: InventorySummary;
  shortages: MaterialShortage[];
  delayedOrders: DelayedOrder[];
  lowStock: LowStockProduct[];
}
