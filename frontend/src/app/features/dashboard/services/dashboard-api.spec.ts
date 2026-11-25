import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

import { DashboardApi } from './dashboard-api';

describe('DashboardApi', () => {
  let service: DashboardApi;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(DashboardApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
