
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';

import {
  provideHttpClientTesting,
  HttpTestingController
} from '@angular/common/http/testing';

import { AiChatApi } from './ai-chat-api';

import {
  API_BASE_URL
} from '../../../core/config/api.config';

describe('AiChatApi', () => {

  let service: AiChatApi;
  let httpMock: HttpTestingController;

  beforeEach(() => {

    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(AiChatApi);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should send a message to the AI endpoint', () => {

    const question = 'Jakich materiałów brakuje?';

    const mockResponse = {
      answer: 'Brakuje 650 nakrętek M8.'
    };

    let result: unknown;

    service.sendMessage(question).subscribe(response => {
      result = response;
    });

    const request = httpMock.expectOne(
      `${API_BASE_URL}/ai/chat`
    );

    expect(request.request.method).toBe('POST');

    expect(request.request.body).toEqual({
      message: question
    });

    request.flush(mockResponse);

    expect(result).toEqual(mockResponse);
  });

  it('should propagate API errors', () => {

    let status: number | undefined;

    service.sendMessage('Test question').subscribe({
      next: () => {
        throw new Error('Expected an API error');
      },
      error: error => {
        status = error.status;
      }
    });

    const request = httpMock.expectOne(
      `${API_BASE_URL}/ai/chat`
    );

    request.flush(
      { detail: 'Service unavailable' },
      {
        status: 503,
        statusText: 'Service Unavailable'
      }
    );

    expect(status).toBe(503);
  });
});
