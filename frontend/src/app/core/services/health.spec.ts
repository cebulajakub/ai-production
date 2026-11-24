import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing';

import { Health } from './health';
import { API_BASE_URL } from '../config/api.config';

describe('Health', () => {

  let service: Health;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(Health);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should send GET request to health endpoint', () => {

    const mockResponse = { status: 'ok' };

    let result: unknown;

    service.checkHealth().subscribe(response => {
      result = response;
    });

    const request = httpMock.expectOne(
      `${API_BASE_URL}/health`
    );

    expect(request.request.method).toBe('GET');

    request.flush(mockResponse);

    expect(result).toEqual(mockResponse);
  });

});
