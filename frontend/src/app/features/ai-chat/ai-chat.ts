
import {
  Component,
  DestroyRef,
  inject,
  signal
} from '@angular/core';

import {
  FormControl,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs';

import { AiChatApi } from './services/ai-chat-api';
import { ChatMessage } from './models/chat.models';
import { getApiErrorMessage } from '../../core/utils/api-error';
import { MarkdownPipe } from '../../core/pipes/markdown-pipe';

@Component({
  selector: 'app-ai-chat',
  imports: [ReactiveFormsModule, MarkdownPipe],
  templateUrl: './ai-chat.html',
  styleUrl: './ai-chat.scss'
})
export class AiChat {

  private readonly aiChatService = inject(AiChatApi);
  private readonly destroyRef = inject(DestroyRef);

  readonly messages = signal<ChatMessage[]>([]);
  readonly isLoading = signal(false);
  readonly error = signal<string | null>(null);

  readonly failedMessage = signal<string | null>(null);

  readonly messageControl = new FormControl('', {
    nonNullable: true,
    validators: [
      Validators.required,
      Validators.maxLength(2000)
    ]
  });

  sendMessage(): void {

    const message = this.messageControl.value.trim();

    if (
      this.messageControl.invalid ||
      !message ||
      this.isLoading()
    ) {
      return;
    }

    this.addMessage('user', message);
    this.messageControl.reset();

    this.requestAnswer(message);
  }

  retryMessage(): void {

    const message = this.failedMessage();

    if (!message || this.isLoading()) {
      return;
    }

    this.requestAnswer(message);
  }

  private requestAnswer(message: string): void {

    this.error.set(null);
    this.failedMessage.set(null);
    this.isLoading.set(true);

    this.aiChatService.sendMessage(message)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => {
          this.isLoading.set(false);
        })
      )
      .subscribe({

        next: response => {
          this.addMessage('assistant', response.answer);
        },

        error: (error: unknown) => {
          this.error.set(getApiErrorMessage(error));
          this.failedMessage.set(message);
        }

      });
  }

  private addMessage(
    role: ChatMessage['role'],
    content: string
  ): void {

    const message: ChatMessage = {
      id: crypto.randomUUID(),
      role,
      content,
      createdAt: new Date()
    };

    this.messages.update(current => [
      ...current,
      message
    ]);
  }
}
