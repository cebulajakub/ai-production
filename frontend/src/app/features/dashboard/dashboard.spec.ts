import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { Dashboard } from './dashboard';
import { DashboardApi } from './services/dashboard-api';
import { DashboardData } from './models/dashboard.models';

describe('Dashboard', () => {
  let component: Dashboard;
  let fixture: ComponentFixture<Dashboard>;

  const mockData: DashboardData = {
    summary: {
      total_products_with_shortages: 1,
      high_priority: 1,
      medium_priority: 0,
      low_priority: 0
    },
    shortages: [
      {
        sku: 'TEST-001',
        product_name: 'Test material',
        total_demand: 100,
        quantity_on_hand: 40,
        shortage: 60,
        severity: 'HIGH'
      }
    ],
    delayedOrders: [],
    lowStock: []
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Dashboard],
      providers: [
        provideRouter([]),
        {
          provide: DashboardApi,
          useValue: {
            getDashboardData: () => of(mockData)
          }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(Dashboard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the dashboard', () => {
    expect(component).toBeTruthy();
  });

  it('should calculate production KPIs', () => {
    expect(component.totalShortages()).toBe(60);
    expect(component.totalDemand()).toBe(100);
    expect(component.summary()?.high_priority).toBe(1);
    expect(component.isLoading()).toBe(false);
  });
});
