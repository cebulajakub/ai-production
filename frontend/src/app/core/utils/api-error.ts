import { HttpErrorResponse } from '@angular/common/http';
import { TimeoutError } from 'rxjs';

export function getApiErrorMessage(error: unknown): string {

  if (error instanceof TimeoutError) {
    return 'The request timed out. Please try again.';
  }

  if (error instanceof HttpErrorResponse) {

    switch (error.status) {

      case 0:
        return 'Unable to connect to the server. Check API availability.';

      case 400:
      case 422:
        return 'Invalid request. Please check your input.';

      case 401:
        return 'Authentication is required.';

      case 403:
        return 'You do not have permission to perform this action.';

      case 429:
        return 'Too many requests. Please try again later.';

      case 500:
        return 'An internal server error occurred.';

      case 502:
      case 503:
      case 504:
        return 'The service is temporarily unavailable. Please try again later.';

      default:
        return 'An unexpected API error occurred.';
    }
  }

  return 'An unexpected error occurred. Please try again.';
}
