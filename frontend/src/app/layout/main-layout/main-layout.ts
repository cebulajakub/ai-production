import {
  Component,
  inject,
  signal,
  OnInit
} from '@angular/core';
import {
  RouterOutlet,
  RouterLink,
  RouterLinkActive
} from '@angular/router';
import { Health } from '../../core/services/health';
import { timeout } from 'rxjs';


@Component({
  selector: 'app-main-layout',
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive
  ],
  templateUrl: './main-layout.html',
  styleUrl: './main-layout.scss'
})
export class MainLayout implements OnInit {

  readonly navigation = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'AI Chat', path: '/ai-chat' },
    { label: 'Inventory', path: '/inventory' },
    { label: 'Orders', path: '/orders' },
    { label: 'Knowledge Base', path: '/knowledge' },
    { label: 'AI Evaluation', path: '/evaluation' }
  ];

  private readonly healthService = inject(Health);

  readonly apiStatus = signal<
    'checking' | 'online' | 'offline'
  >('checking');

  ngOnInit(): void {
    this.checkApiHealth();
  }

  checkApiHealth(): void {

    this.apiStatus.set('checking');

    this.healthService.checkHealth()
      .pipe(timeout(5000))
      .subscribe({
        next: () => {
          this.apiStatus.set('online');
        },
        error: () => {
          this.apiStatus.set('offline');
        }
      });
  }
}
