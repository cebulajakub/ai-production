import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class Health {

  private readonly http = inject(HttpClient);

  checkHealth(): Observable<unknown> {
    return this.http.get<unknown>(
      `${API_BASE_URL}/health`
    );
  }

}
