import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, timeout } from 'rxjs';

import {
  API_BASE_URL,
  AI_REQUEST_TIMEOUT_MS
} from '../../../core/config/api.config';

import {
  ChatRequest,
  ChatResponse
} from '../models/chat.models';


@Injectable({
  providedIn: 'root'
})
export class AiChatApi {

  private readonly http = inject(HttpClient);

  sendMessage(message: string): Observable<ChatResponse> {

    const request: ChatRequest = {
      message
    };

    return this.http.post<ChatResponse>(
      `${API_BASE_URL}/ai/chat`,
      request
    ).pipe(
      timeout(AI_REQUEST_TIMEOUT_MS)
    );
  }
}
