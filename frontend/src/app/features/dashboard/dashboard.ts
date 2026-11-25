
import {
  Component,
  computed,
  DestroyRef,
  inject,
  OnInit,
  signal
} from '@angular/core';

import { DecimalPipe, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs';

import { DashboardApi } from './services/dashboard-api';
import { DashboardData } from './models/dashboard.models';
import { getApiErrorMessage } from '../../core/utils/api-error';

@Component({
  selector: 'app-dashboard',
  imports: [DecimalPipe, DatePipe, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {

  private readonly dashboardApi = inject(DashboardApi);
  private readonly destroyRef = inject(DestroyRef);

  readonly data = signal<DashboardData | null>(null);
  readonly isLoading = signal(false);
  readonly error = signal<string | null>(null);
  readonly lastUpdated = signal<Date | null>(null);

  readonly summary = computed(() => this.data()?.summary ?? null);

  readonly shortages = computed(() =>
    this.data()?.shortages ?? []
  );

  readonly delayedOrders = computed(() =>
    this.data()?.delayedOrders ?? []
  );

  readonly lowStock = computed(() =>
    this.data()?.lowStock ?? []
  );

  readonly totalShortages = computed(() =>
    this.shortages().reduce(
      (total, item) => total + item.shortage, 0
    )
  );

  readonly totalDemand = computed(() =>
    this.shortages().reduce(
      (total, item) => total + item.total_demand, 0
    )
  );

  readonly maxShortage = computed(() =>
    Math.max(1, ...this.shortages().map(item => item.shortage))
  );

  readonly severityGradient = computed(() => {

    const summary = this.summary();

    if (!summary || !summary.total_products_with_shortages) {
      return '#334155';
    }

    const total = summary.total_products_with_shortages;

    const high = summary.high_priority / total * 100;

    const medium =
      (summary.high_priority + summary.medium_priority)
      / total * 100;

    return `conic-gradient(
      #f87171 0% ${high}%,
      #fbbf24 ${high}% ${medium}%,
      #818cf8 ${medium}% 100%
    )`;
  });

  readonly kpis = computed(() => [
    {
      label: 'Total Shortages',
      value: this.totalShortages(),
      description: 'Missing material quantity',
      icon: '↓',
      color: 'red'
    },
    {
      label: 'Affected Materials',
      value: this.summary()?.total_products_with_shortages ?? 0,
      description: 'Materials with shortages',
      icon: '▦',
      color: 'purple'
    },
    {
      label: 'Critical Shortages',
      value: this.summary()?.high_priority ?? 0,
      description: 'High priority materials',
      icon: '!',
      color: 'red'
    },
    {
      label: 'Delayed Orders',
      value: this.delayedOrders().length,
      description: 'Orders in returned page',
      icon: '◷',
      color: 'amber'
    },
    {
      label: 'Low Stock',
      value: this.lowStock().length,
      description: 'Materials below stock threshold',
      icon: '▤',
      color: 'blue'
    },
    {
      label: 'Material Demand',
      value: this.totalDemand(),
      description: 'Demand for shortage materials',
      icon: '↗',
      color: 'green'
    }
  ]);

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {

    if (this.isLoading()) return;

    this.isLoading.set(true);
    this.error.set(null);

    this.dashboardApi.getDashboardData()
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.isLoading.set(false))
      )
      .subscribe({
        next: data => {
          this.data.set(data);
          this.lastUpdated.set(new Date());
        },
        error: (error: unknown) => {
          this.error.set(getApiErrorMessage(error));
        }
      });
  }

  getShortagePercentage(shortage: number): number {
    return shortage / this.maxShortage() * 100;
  }
}
