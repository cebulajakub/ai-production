
import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {
  forkJoin,
  Observable,
  timeout
} from 'rxjs';

import { API_BASE_URL } from '../../../core/config/api.config';

import {
  DashboardData,
  InventorySummary,
  MaterialShortage,
  DelayedOrder,
  LowStockProduct
} from '../models/dashboard.models';

@Injectable({
  providedIn: 'root'
})
export class DashboardApi {

  private readonly http = inject(HttpClient);

  getInventorySummary(): Observable<InventorySummary> {
    return this.http.get<InventorySummary>(
      `${API_BASE_URL}/inventory/summary`
    );
  }

  getMaterialShortages(): Observable<MaterialShortage[]> {
    return this.http.get<MaterialShortage[]>(
      `${API_BASE_URL}/inventory/shortages`
    );
  }

  getDelayedOrders(): Observable<DelayedOrder[]> {
    return this.http.get<DelayedOrder[]>(
      `${API_BASE_URL}/orders/delayed`
    );
  }

  getLowStock(): Observable<LowStockProduct[]> {
    return this.http.get<LowStockProduct[]>(
      `${API_BASE_URL}/inventory/low-stock`
    );
  }

  getDashboardData(): Observable<DashboardData> {

    return forkJoin({
      summary: this.getInventorySummary(),
      shortages: this.getMaterialShortages(),
      delayedOrders: this.getDelayedOrders(),
      lowStock: this.getLowStock()
    }).pipe(
      timeout(15_000)
    );

  }
}
